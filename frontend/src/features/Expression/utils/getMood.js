export const getMood = (bs, current) => {
  const smile = (bs.mouthSmileLeft + bs.mouthSmileRight) / 2;
  const frown = (bs.mouthFrownLeft + bs.mouthFrownRight) / 2;
  const press = (bs.mouthPressLeft + bs.mouthPressRight) / 2;

  const sad =
    bs.browInnerUp * 0.3 +
    frown * 0.4 +
    bs.mouthShrugLower * 0.2 +
    bs.mouthRollLower * 0.2 +
    press * 0.1;

  const sadLimit = current === '😢 SAD' ? 0.1 : 0.15;

  if (smile > 0.4) return '😊 HAPPY';
  if (bs.jawOpen > 0.4 && bs.browInnerUp > 0.3) return '😮 SURPRISE';
  if (sad > sadLimit) return '😢 SAD';
  return '😐 NEUTRAL';
};
