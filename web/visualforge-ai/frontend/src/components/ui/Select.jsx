export default function Select({ className = "", children, ...props }) {
  return (
    <select
      className={`focus-ring h-11 w-full rounded-md border border-white/[0.12] bg-forge-panel px-3 text-sm text-forge-text transition hover:border-white/[0.18] focus:border-forge-primary ${className}`}
      {...props}
    >
      {children}
    </select>
  );
}
