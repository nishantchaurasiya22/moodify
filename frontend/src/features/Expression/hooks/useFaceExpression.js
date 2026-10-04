import { useEffect, useRef, useState } from 'react';
import { FaceLandmarker, FilesetResolver } from '@mediapipe/tasks-vision';
import { getMood } from '../utils/getMood';

const MODEL = import.meta.env.VITE_MODEL_URL;
const WASM = import.meta.env.VITE_WASM_URL;

export const useFaceExpression = () => {
  const videoRef = useRef(null);
  const rafId = useRef();
  const stream = useRef();
  const landmarker = useRef();
  const [mood, setMood] = useState('');
  const [started, setStarted] = useState(false);

  const start = async () => {
    setStarted(true);
    setMood('⏳ LOADING...');

    const vision = await FilesetResolver.forVisionTasks(WASM);
    landmarker.current = await FaceLandmarker.createFromOptions(vision, {
      baseOptions: { modelAssetPath: MODEL },
      runningMode: 'VIDEO',
      outputFaceBlendshapes: true,
    });

    stream.current = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream.current;
    await videoRef.current.play();

    let current = '😐 NEUTRAL';
    const smooth = {};

    const loop = () => {
      const cats = landmarker.current.detectForVideo(videoRef.current, performance.now())
        .faceBlendshapes?.[0]?.categories;

      if (cats) {
        cats.forEach((c) => {
          smooth[c.categoryName] = (smooth[c.categoryName] ?? c.score) * 0.8 + c.score * 0.2;
        });
        current = getMood(smooth, current);
        setMood(current);
      } else {
        setMood('👤 NO FACE DETECTED');
      }
      rafId.current = requestAnimationFrame(loop);
    };
    loop();
  };

  useEffect(() => {
    return () => {
      cancelAnimationFrame(rafId.current);
      stream.current?.getTracks().forEach((t) => t.stop());
      landmarker.current?.close();
    };
  }, []);

  return { videoRef, mood, started, start };
};