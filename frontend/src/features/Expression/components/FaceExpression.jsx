import { useFaceExpression } from '../hooks/useFaceExpression';

const FaceExpression = () => {
  const { videoRef, mood, started, start } = useFaceExpression();

  return (
    <div className='detect-part'>
      <video ref={videoRef} playsInline muted />
      <button onClick={start} disabled={started}>Start Face Detecting</button>
      <h1>{mood}</h1>
    </div>
  );
};

export default FaceExpression;