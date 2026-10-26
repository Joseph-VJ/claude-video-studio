import React from 'react';

/* ---------------------------------------------------------------------------------------------------------------
   DESIGN TOKENS: the only place hex values, radii, shadows and easing live (see .context/DESIGN.md, rev d1).
   --------------------------------------------------------------------------------------------------------------- */
export const T = {
  groundHi: '#27397A', ground: '#22326A', groundLo: '#1B2759',
  ink: '#14193A', paper: '#F3EADC', paperDim: '#E7DCC9',
  accent: '#E5A63A', accentDeep: '#B8801F',
  alert: '#B13B34', alertDeep: '#7E3733',
  good: '#3FB594',
  mutedOnGround: 'rgba(243,234,220,0.72)', mutedOnPaper: 'rgba(20,25,58,0.62)', hairline: 'rgba(243,234,220,0.92)',
};
export const R = {card: 28, chip: 18, window: 40};
export const SH = {low: '0 6px 16px rgba(10,14,40,0.30)', high: '0 18px 44px rgba(10,14,40,0.38)'};
export const FONT = "'Archivo', 'Nirmala UI', 'Segoe UI', sans-serif";
export const FPS = 30;
export const ENTER = 12;   // frames, entrances
export const LEAVE = 5;    // frames, exits (shorter than entrances)

export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const prog = (lf: number, start: number, dur: number) => clamp((lf - start) / dur);
export const eOut = (t: number) => 1 - Math.pow(1 - t, 3);                       // power3.out
export const eExpo = (t: number) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t));      // ~cubic-bezier(.16,1,.3,1)
export const eIn = (t: number) => t * t * t;                                     // exits accelerate
export const eInOut = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
export const rnd = (n: number) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

/** no-overshoot arrival 0 -> 1 starting at frame `at` (replaces the v1 spring) */
export const arrive = (lf: number, at: number, dur = ENTER) => eExpo(clamp((lf - at) / dur));

type PopProps = {c?: boolean; lf: number; at: number; x: number; y: number; w?: number; h?: number; from?: 'rise' | 'left' | 'right' | 'top' | 'bottom' | 'scale'; rot?: number; z?: number; children: React.ReactNode; out?: number; style?: React.CSSProperties; origin?: string};
/** absolutely positioned element: eased entrance at `at` (12 f), shorter accelerating exit at `out` (5 f). `rot` is only for the two declared stamps. */
export const Pop: React.FC<PopProps> = ({c, lf, at, x, y, w, h, from = 'rise', rot = 0, z = 1, children, out, style, origin = '50% 50%'}) => {
  if (lf < at) return null;
  const p = arrive(lf, at);
  const o = clamp((lf - at) / 6);
  const q = out !== undefined ? eIn(clamp((lf - out) / LEAVE)) : 0;
  if (q >= 1) return null;
  let tx = 0, ty = 0;
  if (from === 'rise') ty = (1 - p) * 40;
  if (from === 'left') tx = -(1 - p) * 160;
  if (from === 'right') tx = (1 - p) * 160;
  if (from === 'top') ty = -(1 - p) * 120;
  if (from === 'bottom') ty = (1 - p) * 120;
  ty -= q * 16;
  const sc = 0.97 + 0.03 * p;
  return <div style={{position: 'absolute', left: x, top: y, width: w, height: h, opacity: o * (1 - q), transform: `${c ? 'translateX(-50%) ' : ''}translate(${tx}px,${ty}px) scale(${sc}) rotate(${rot * p}deg)`, transformOrigin: origin, zIndex: z, ...style}}>{children}</div>;
};

/* ------------------------------------------------ text ------------------------------------------------ */
export type Variant = 'ink' | 'punch' | 'paper' | 'hero' | 'alert' | 'good' | 'plain';
const VAR: Record<Variant, {bg: string; fg: string}> = {
  ink: {bg: T.ink, fg: T.paper}, punch: {bg: T.ink, fg: T.accent}, paper: {bg: T.paper, fg: T.ink}, hero: {bg: T.accent, fg: T.ink},
  alert: {bg: T.alert, fg: T.paper}, good: {bg: T.good, fg: T.ink}, plain: {bg: 'transparent', fg: T.paper},
};
/** the one text style: chip variants ink / paper / hero / alert / good, or plain text. Large sizes use the semi-condensed width. */
export const Chip: React.FC<{text: string; v?: Variant; size?: number; padX?: number; tamil?: boolean; fg?: string; style?: React.CSSProperties}> = ({text, v = 'paper', size = 56, padX, tamil, fg, style}) => {
  const c = VAR[v];
  const big = size >= 100, mid = size >= 54 && size < 100;
  const px = v === 'plain' ? 0 : padX ?? size * 0.4;
  return (
    <div style={{display: 'inline-block', background: c.bg, color: fg ?? c.fg, fontFamily: FONT, fontWeight: 800, fontStretch: big ? '82%' : mid ? '90%' : '100%', fontSize: size, lineHeight: tamil ? 1.35 : 1.05, letterSpacing: big ? '-0.01em' : mid ? '0' : '0.02em', padding: v === 'plain' ? 0 : `${px * 0.5}px ${px}px`, borderRadius: R.chip, whiteSpace: 'nowrap', boxShadow: v === 'plain' ? undefined : SH.low, textShadow: v === 'plain' ? '0 2px 12px rgba(10,14,40,0.55)' : undefined, ...style}}>{text}</div>
  );
};
/** small caps label */
export const Label: React.FC<{text: string; color?: string; size?: number}> = ({text, color = T.mutedOnGround, size = 30}) => (
  <div style={{fontFamily: FONT, fontWeight: 600, fontSize: size, color, letterSpacing: '0.08em', textTransform: 'uppercase'}}>{text}</div>
);

export const Counter: React.FC<{lf: number; at: number; dur?: number; from?: number; to: number; prefix?: string; suffix?: string; size: number; color?: string; fmt?: (n: number) => string; weight?: number; style?: React.CSSProperties}> = ({lf, at, dur = 26, from = 0, to, prefix = '', suffix = '', size, color = T.paper, fmt, weight = 800, style}) => {
  const p = eOut(prog(lf, at, dur));
  const v = from + (to - from) * p;
  const s = fmt ? fmt(v) : Math.round(v).toLocaleString('en-IN');
  return <span style={{fontFamily: FONT, fontWeight: weight, fontStretch: '88%', fontSize: size, color, letterSpacing: '-0.01em', fontVariantNumeric: 'tabular-nums', ...style}}>{prefix}{s}{suffix}</span>;
};

export const Card: React.FC<{w: number; h: number; bg?: string; r?: number; elev?: 'low' | 'high'; children?: React.ReactNode; style?: React.CSSProperties}> = ({w, h, bg = T.paper, r = R.card, elev = 'high', children, style}) => (
  <div style={{width: w, height: h, borderRadius: r, background: bg, boxShadow: SH[elev], position: 'relative', overflow: 'hidden', ...style}}>{children}</div>
);

/* ------------------------------------------------ icons: flat vector, palette only, stroke 8 ------------------------------------------------ */
export const Disc: React.FC<{letter: string; color: string; size?: number; fg?: string}> = ({letter, color, size = 150, fg = T.paper}) => (
  <div style={{width: size, height: size, borderRadius: size, background: color, color: fg, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 800, fontStretch: '88%', fontSize: size * 0.62, lineHeight: 1, boxShadow: SH.low}}>{letter}</div>
);

export const Building: React.FC<{w?: number; h?: number; color?: string; win?: string}> = ({w = 300, h = 380, color = T.paper, win = T.ground}) => {
  const cols = 3, rows = 6;
  return (
    <svg viewBox="0 0 300 380" width={w} height={h}>
      <rect x="40" y="30" width="220" height="350" rx="14" fill={color} />
      <rect x="120" y="0" width="60" height="40" rx="8" fill={color} />
      {Array.from({length: rows * cols}).map((_, i) => <rect key={i} x={68 + (i % cols) * 66} y={58 + Math.floor(i / cols) * 46} width="38" height="28" rx="6" fill={win} opacity={0.4 + 0.6 * rnd(i + 3)} />)}
      <rect x="118" y="320" width="64" height="60" rx="10" fill={win} />
    </svg>
  );
};

export const Check: React.FC<{size?: number; p: number; color?: string; bg?: string}> = ({size = 90, p, color = T.ink, bg = T.good}) => (
  <svg viewBox="0 0 100 100" width={size} height={size}>
    <circle cx="50" cy="50" r="48" fill={bg} />
    <path d="M26 52 L44 70 L76 32" fill="none" stroke={color} strokeWidth="11" strokeLinecap="round" strokeLinejoin="round" strokeDasharray={90} strokeDashoffset={90 * (1 - clamp(p))} />
  </svg>
);

export const Cross: React.FC<{size?: number; bg?: string; color?: string}> = ({size = 90, bg = T.alert, color = T.paper}) => (
  <svg viewBox="0 0 100 100" width={size} height={size}><circle cx="50" cy="50" r="48" fill={bg} /><path d="M32 32 L68 68 M68 32 L32 68" stroke={color} strokeWidth="11" strokeLinecap="round" /></svg>
);

/** flat coin: accent disc, deep rim, ink rupee */
export const Coin: React.FC<{size?: number}> = ({size = 120}) => (
  <svg viewBox="0 0 100 100" width={size} height={size}>
    <circle cx="50" cy="50" r="48" fill={T.accentDeep} /><circle cx="50" cy="50" r="42" fill={T.accent} />
    <text x="50" y="68" textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize="52" fill={T.ink}>₹</text>
  </svg>
);

/** flat stack of three coins (side view); each coin settles onto the pile in turn (4 f apart) */
export const CoinStack: React.FC<{size?: number; lf: number; at: number}> = ({size = 360, lf, at}) => (
  <svg viewBox="0 0 240 200" width={size} height={size * 200 / 240}>
    {[0, 1, 2].map(i => {
      const p = arrive(lf, at + i * 4, 10), y = 126 - i * 44, ox = i === 1 ? 14 : 0;
      return (
        <g key={i} transform={`translate(${ox} ${-(1 - p) * 90})`} opacity={clamp(p * 3)}>
          <rect x="20" y={y} width="200" height="40" rx="20" fill={T.accentDeep} />
          <ellipse cx="120" cy={y + 6} rx="100" ry="26" fill={T.accent} />
          {i === 2 && <text x="120" y={y + 20} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize="52" fill={T.ink}>₹</text>}
        </g>
      );
    })}
  </svg>
);

export const Chevrons: React.FC<{lf: number; at: number; color?: string; w?: number}> = ({lf, at, color = T.accent, w = 220}) => (
  <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0}}>
    {[0, 1, 2].map(i => {
      const t = ((lf - at) * 0.11 - i * 0.55) % 3; const a = clamp(1 - Math.abs(((t + 3) % 3) - 1.0) / 1.0);
      return <svg key={i} viewBox="0 0 100 50" width={w} height={w * 0.5} style={{opacity: 0.2 + 0.8 * a, marginTop: -w * 0.1}}><path d="M10 8 L50 40 L90 8" fill="none" stroke={color} strokeWidth="14" strokeLinecap="round" strokeLinejoin="round" /></svg>;
    })}
  </div>
);

export const Ring: React.FC<{size: number; p: number; color: string; track?: string; width?: number; children?: React.ReactNode}> = ({size, p, color, track = 'rgba(243,234,220,0.2)', width = 26, children}) => {
  const r = (size - width) / 2, circ = 2 * Math.PI * r;
  return (
    <div style={{position: 'relative', width: size, height: size}}>
      <svg width={size} height={size} style={{transform: 'rotate(-90deg)'}}>
        <circle cx={size / 2} cy={size / 2} r={r} stroke={track} strokeWidth={width} fill="none" />
        <circle cx={size / 2} cy={size / 2} r={r} stroke={color} strokeWidth={width} fill="none" strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={circ * (1 - clamp(p))} />
      </svg>
      <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column'}}>{children}</div>
    </div>
  );
};

export const Clock: React.FC<{size?: number; lf: number; color?: string}> = ({size = 90, lf, color = T.ink}) => (
  <svg viewBox="0 0 100 100" width={size} height={size}><circle cx="50" cy="50" r="42" fill="none" stroke={color} strokeWidth="8" /><line x1="50" y1="50" x2="50" y2="22" stroke={color} strokeWidth="8" strokeLinecap="round" transform={`rotate(${lf * 6} 50 50)`} /><line x1="50" y1="50" x2="68" y2="58" stroke={color} strokeWidth="8" strokeLinecap="round" transform={`rotate(${lf * 0.5} 50 50)`} /></svg>
);

export const PhoneIcon: React.FC<{size?: number; color?: string}> = ({size = 120, color = T.ink}) => (
  <svg viewBox="0 0 100 100" width={size} height={size}><path d="M24 12 L40 10 L48 32 L38 40 Q46 58 60 66 L68 58 L90 66 L88 82 Q60 96 30 66 Q4 38 24 12Z" fill={color} /></svg>
);

export const AppIcon: React.FC<{size?: number; color?: string}> = ({size = 110, color = T.ink}) => (
  <svg viewBox="0 0 100 100" width={size} height={size}><rect x="26" y="6" width="48" height="88" rx="12" fill="none" stroke={color} strokeWidth="8" /><rect x="34" y="20" width="32" height="48" rx="4" fill={color} opacity="0.18" /><circle cx="50" cy="80" r="4" fill={color} /><text x="50" y="55" textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize="28" fill={color}>₹</text></svg>
);

export const BankIcon: React.FC<{size?: number; color?: string}> = ({size = 110, color = T.ink}) => (
  <svg viewBox="0 0 100 100" width={size} height={size}><path d="M50 8 L92 30 L8 30Z" fill={color} /><rect x="14" y="36" width="12" height="38" fill={color} /><rect x="38" y="36" width="12" height="38" fill={color} /><rect x="62" y="36" width="12" height="38" fill={color} /><rect x="6" y="80" width="88" height="12" rx="3" fill={color} /></svg>
);
