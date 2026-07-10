export default function Input({ className = "", as = "input", ...props }) {
  const Tag = as;
  return (
    <Tag
      className={`focus-ring w-full rounded-md border border-white/[0.12] bg-white/[0.06] px-3 py-2.5 text-sm text-forge-text placeholder:text-forge-muted/70 transition hover:border-white/[0.18] focus:border-forge-primary ${className}`}
      {...props}
    />
  );
}
