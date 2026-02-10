import { useState } from "react";

type CopyButtonProps = {
  text: string;
  label?: string;
  className?: string;
};

export default function CopyButton({
  text,
  label = "📋 Copy to Clipboard",
  className = "",
}: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    if (!text) return;

    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);

      // Reset label after 2 seconds
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error("Failed to copy text:", error);
    }
  };

  return (
    <button
      onClick={handleCopy}
      className={className}
      style={{
        padding: "8px 12px",
        borderRadius: 6,
        border: "1px solid #ccc",
        cursor: "pointer",
        backgroundColor: copied ? "#e6fffa" : "#ffffff",
      }}
      aria-label="Copy content to clipboard"
    >
      {copied ? "✅ Copied!" : label}
    </button>
  );
}
