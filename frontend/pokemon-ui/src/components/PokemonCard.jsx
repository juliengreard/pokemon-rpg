import StatusIcon from "./StatusIcon";

export default function PokemonCard({
  poke,
  team,
  inBattle = false,
  selectable = true,
  updatePokemonHp,
  setActivePokemon,
  removeFromTeam,
  affectStatus,
  disableStatus,
  setActive1,
  setActive2,
}) {
  const TYPE_SIZE_CARD = 48;

  return (
    <div
      key={poke.id}
      style={{
        margin: "0.5rem",
        padding: "0.5rem",
        border: "2px solid #ddd",
        borderRadius: "8px",
        width: "220px",
        backgroundColor: "#f9f9f9",
        textAlign: "center",
        position: "relative",
      }}
    >
      {/* Status Icon */}
      <div>
        {poke.status && (
          <StatusIcon
            effect={poke.status}
            text={poke.status_effect_deactivation_chance}
            onClick={() => disableStatus(team, poke.status)}
          />
        )}
      </div>

      {/* Remove Button */}
      {!inBattle && (
        <button
          onClick={() => removeFromTeam(team, poke.id)}
          style={{
            position: "absolute",
            top: "4px",
            right: "4px",
            background: "#f44336",
            color: "white",
            border: "none",
            borderRadius: "50%",
            cursor: "pointer",
            width: "20px",          // ✅ smaller circle
            height: "20px",
            fontSize: "12px",       // ✅ smaller X
            fontWeight: "bold",
            lineHeight: "20px",     // ✅ centers the "X" perfectly
            textAlign: "center",
            padding: 0,
          }}
        >
          ×
        </button>
      )}

      {/* Level */}
      <div
        style={{
          position: "absolute",
          top: "6px",
          left: "6px",
          backgroundColor: "#4CAF50",
          color: "white",
          padding: "2px 8px",
          borderRadius: "12px",
          fontSize: "0.85rem",
          fontWeight: "bold",
        }}
      >
        Lv {poke.level}
      </div>

      <h4>{poke.family}</h4>
      <img
        src={poke.image}
        alt={poke.family}
        width="120"
        style={{ border: "2px solid #ccc", borderRadius: "8px" }}
      />

      {/* Types */}
      <div style={{ marginTop: "0.5rem", display: "flex", gap: "6px", justifyContent: "center" }}>
        {poke.types.map((t, i) => (
          <img
            key={i}
            src={`http://localhost:8000/images/types/${t}.png`}
            alt={t}
            width={TYPE_SIZE_CARD}
          />
        ))}
      </div>

    {/* HP */}
    <div style={{ marginTop: "0.5rem" }}>
      <label>HP: {poke.hp}</label>
      {inBattle ? (
        <input
          type="range"
          min="0"
          max={poke.maxHp}
          value={poke.hp}
          onChange={(e) => updatePokemonHp(team, poke.id, Number(e.target.value))}
          style={{ width: "100%", accentColor: "green" }}
        />
      ) : (
        <div style={{ background: "#ddd", height: "8px", borderRadius: "4px", overflow: "hidden" }}>
          <div
            style={{
              width: `${(poke.hp / poke.maxHp) * 100}%`,
              background: "green",
              height: "100%",
            }}
          />
        </div>
      )}
    </div>


      {/* Moves */}
      <div style={{ marginTop: "1rem", textAlign: "left" }}>
        <h4>Moves:</h4>
        {poke.moves.length > 0 ? (
          <ul style={{ paddingLeft: "1rem" }}>
            {poke.moves.map((m, idx) => (
              <li key={idx} style={{ marginBottom: "0.5rem" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                  <img
                    src={`http://localhost:8000/images/types/move_${m.type}.png`}
                    alt={m.type}
                    width={24}
                  />
                  <strong>{m.name}</strong> {m.power && `(${m.power})`}
                  {m.status_effect && (
                    <StatusIcon
                      effect={m.status_effect}
                      text={m.status_effect_activation_chance}
                      onClick={() =>
                        affectStatus(team, m.status_effect, m.status_effect_deactivation_chance)
                      }
                    />
                  )}
                </div>
                <small>{m.description}</small>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ fontStyle: "italic", color: "#888" }}>No moves</p>
        )}
      </div>

      {/* Battle Buttons */}
      {!inBattle && selectable && (
        <button onClick={() => setActivePokemon(team, poke)}>Send to Battle</button>
      )}

      {inBattle && (
        <button onClick={() => (team === 1 ? setActive1(null) : setActive2(null))}>
          Recall
        </button>
      )}
    </div>
  );
}
