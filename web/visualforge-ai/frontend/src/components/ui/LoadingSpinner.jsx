import Logo2 from "../../assets/Logo2.png";

export default function LoadingSpinner({ label = "Generating" }) {
  return (
    <div className="flex items-center gap-3 text-sm text-forge-muted">
      <span className="grid h-9 w-9 place-items-center rounded-md border border-forge-primary/30 bg-forge-primary/10">
        <img src={Logo2} alt="" className="h-5 w-5 animate-pulse object-contain" />
      </span>
      <span>{label}</span>
    </div>
  );
}
