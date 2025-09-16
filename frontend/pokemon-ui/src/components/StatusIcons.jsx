import React, { useState } from "react";

const STATUS_ICONS = {
  Poison: {
    image: "http://localhost:8000/images/status/poison.jpg",
    label: "Poison",
    color: "green",
  }
};

export default function StatusIcon({ effect, text, onClick }) {
  console.log("on click : ", onClick);
  const [hover, setHover] = useState(false);

  if (!effect || !STATUS_ICONS[effect]) return null;

  const { image, label, color } = STATUS_ICONS[effect];
  return (
    <div
      style={{
        position: "relative",
        display: "inline-block",
        marginRight: "8px",
      }}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
    >
      <img
        src={image}
        alt={label}
        style={{
          width: "16px",
          height: "16px",
          cursor: "pointer",
          border: `1px solid ${color}`,
          borderRadius: "4px",
        }}
        onClick={onClick}
      />
      {hover && (
        <div
          style={{
            position: "absolute",
            bottom: "100%",
            left: "50%",
            transform: "translateX(-50%)",
            marginBottom: "4px",
            backgroundColor: "#333",
            color: "#fff",
            fontSize: "12px",
            padding: "4px 8px",
            borderRadius: "4px",
            whiteSpace: "nowrap",
            boxShadow: "0px 2px 6px rgba(0,0,0,0.3)",
            zIndex: 10,
          }}
        >
          {label}: {text ? `${text}` : ""}
        </div>
      )}
    </div>
  );
}
