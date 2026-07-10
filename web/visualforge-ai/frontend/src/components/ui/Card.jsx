export default function Card({ children, className = "", as: Tag = "section" }) {
  return <Tag className={`glass-card rounded-lg ${className}`}>{children}</Tag>;
}
