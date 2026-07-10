const domains = [
  { value: "base", label: "General / Base" },
  { value: "product_ads", label: "Product Ads" },
  { value: "egyptian_cultural", label: "Egyptian Cultural" },
];

export default function DomainSelector({ value, onChange }) {
  return (
    <div className="flex flex-wrap gap-2">
      {domains.map((domain) => (
        <button
          key={domain.value}
          type="button"
          onClick={() => onChange(domain.value)}
          className={`focus-ring h-10 rounded-md border px-3 text-sm font-semibold transition ${
            value === domain.value
              ? "border-forge-secondary bg-forge-secondary/20 text-forge-text"
              : "border-white/[0.12] bg-white/[0.04] text-forge-muted hover:text-forge-text"
          }`}
        >
          {domain.label}
        </button>
      ))}
    </div>
  );
}
