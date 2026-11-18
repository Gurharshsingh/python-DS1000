import { Info, AlertTriangle, Lightbulb, CheckCircle2 } from "lucide-react";

interface CalloutProps {
  type?: "info" | "warning" | "tip" | "success";
  title?: string;
  children: React.ReactNode;
}

export function Callout({ type = "info", title, children }: CalloutProps) {
  const icons = {
    info: <Info size={18} className="text-blue-500" />,
    warning: <AlertTriangle size={18} className="text-amber-500" />,
    tip: <Lightbulb size={18} className="text-accent" />,
    success: <CheckCircle2 size={18} className="text-emerald-500" />,
  };

  const borders = {
    info: "border-blue-500/30 bg-blue-500/5 text-text",
    warning: "border-amber-500/30 bg-amber-500/5 text-text",
    tip: "border-accent/30 bg-accent/5 text-text",
    success: "border-emerald-500/30 bg-emerald-500/5 text-text",
  };

  return (
    <div className={`my-6 rounded-[var(--radius-md)] border p-4 ${borders[type]}`}>
      <div className="flex items-start gap-3">
        <div className="mt-0.5 shrink-0">{icons[type]}</div>
        <div className="w-full text-sm leading-relaxed">
          {title && <p className="mb-1 font-semibold text-text">{title}</p>}
          <div className="prose-sm text-text-muted [&>p]:m-0">{children}</div>
        </div>
      </div>
    </div>
  );
}
