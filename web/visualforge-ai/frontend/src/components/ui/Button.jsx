const variants = {
  primary:
    "bg-forge-primary text-slate-950 hover:bg-sky-300 disabled:bg-slate-600 disabled:text-slate-300",
  secondary:
    "bg-white/[0.08] text-forge-text border border-white/[0.12] hover:bg-white/[0.12] disabled:text-slate-500",
  ghost: "text-forge-muted hover:text-forge-text hover:bg-white/[0.08] disabled:text-slate-600",
  danger:
    "bg-forge-error/[0.18] text-red-100 border border-forge-error/30 hover:bg-forge-error/[0.28]",
};

const sizes = {
  sm: "h-9 px-3 text-sm",
  md: "h-11 px-4 text-sm",
  lg: "h-12 px-5 text-base",
  icon: "h-10 w-10 p-0",
};

export default function Button({
  children,
  className = "",
  variant = "primary",
  size = "md",
  type = "button",
  ...props
}) {
  return (
    <button
      type={type}
      className={`focus-ring inline-flex items-center justify-center gap-2 rounded-md font-semibold transition disabled:cursor-not-allowed ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
