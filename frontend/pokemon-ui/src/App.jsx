import { useState } from "react";
import axios from "axios";

// 🔧 tweak sizes
const TYPE_SIZE_MAIN = 72;
const TYPE_SIZE_CARD = 48;

function PokemonCard({
  poke,
  team,
  isPreview = false,
  onRemove,
  onHpChange,
  onAssign,
  onSelect,
  isActive,
}) {
  if (!poke) return null;

  return (
    <div
      style={{
        margin: "0.5rem",
        padding: "0.5rem",
        border: "2px solid #ddd",
        borderRadius: "8px",
        width: isPreview ? "280px" : "200px",
        backgroundColor: isActive ? "#e0ffe0" : "#f9f9f9",
        textAlign: "center",
        position: "relative",
      }}
    >
      {/* Remove (only in team) */}
      {!isPreview && onRemove && (
        <button
          onClick={onRemove}
          style={{
            position: "absolute",
            top: "6px",
            right: "6px",
            width: "28px",
            height: "28px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            background: "red",
            color: "white",
            border: "none",
            borderRadius: "50%",
            cursor: "pointer",
            fontSize: "18px",
            fontWeight: 700,
          }}
        >
          ×
        </button>
      )}

      {/* Level badge */}
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

      <h4 style={{ marginTop: "1.25rem" }}>{poke.name}</h4>
      <img
        src={poke.image}
        alt={poke.name}
        width={isPreview ? 170 : 120}
        style={{
          border: "2px solid #ccc",
          borderRadius: "8px",
          marginTop: "0.5rem",
        }}
      />

      {/* Type icons */}
      <div
        style={{
          marginTop: "0.5rem",
          display: "flex",
          gap: "6px",
          justifyContent: "center",
          flexWrap: "wrap",
        }}
      >
        {poke.types.map((t, i) => (
          <img
            key={i}
            src={`http://localhost:8000/images/types/${t}.png`}
            alt={t}
            width={isPreview ? TYPE_SIZE_MAIN : TYPE_SIZE_CARD}
          />
        ))}
      </div>

      {/* HP slider */}
      <div style={{ marginTop: "0.5rem" }}>
        <label>HP: {poke.hp}</label>
        <input
          type="range"
          min="0"
          max={poke.maxHp}
          value={poke.hp}
          onChange={(e) =>
            onHpChange && onHpChange(Number(e.target.value))
          }
          style={{ width: "100%", accentColor: "green" }}
        />
      </div>

      {/* Moves */}
      <div style={{ marginTop: "1rem", textAlign: "left" }}>
        <h4 style={{ marginBottom: "0.5rem" }}>Moves:</h4>
        {poke.moves.length > 0 ? (
          <ul style={{ paddingLeft: "1rem" }}>
            {poke.moves.map((move, idx) => (
              <li
                key={idx}
                style={{
                  marginBottom: "0.5rem",
                  padding: "0.25rem",
                  border: "1px solid #ccc",
                  borderRadius: "6px",
                  display: "flex",
                  flexDirection: "column",
                  backgroundColor: "#f0f0f0",
                }}
              >
                <div
                  style={{
                    fontWeight: "bold",
                    fontSize: "0.95rem",
                    display: "flex",
                    alignItems: "center",
                    gap: "6px",
                  }}
                >
                  <img
                    src={`http://localhost:8000/images/types/move_${move.type}.png`}
                    alt={move.type}
                    width={32}
                  />
                  {move.name} {move.power && `(Power: ${move.power})`}
                </div>
                <div
                  style={{
                    fontSize: "0.85rem",
                    color: "#555",
                    marginTop: "2px",
                  }}
                >
                  {move.description}
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ fontStyle: "italic", color: "#888" }}>
            No moves available
          </p>
        )}
      </div>

      {/* Action buttons */}
      {isPreview && onAssign && (
        <div style={{ marginTop: "1rem" }}>
          <button onClick={() => onAssign(1)}>Assign to Team 1</button>
          <button
            onClick={() => onAssign(2)}
            style={{ marginLeft: "0.5rem" }}
          >
            Assign to Team 2
          </button>
        </div>
      )}

      {!isPreview && onSelect && (
        <div style={{ marginTop: "0.5rem" }}>
          <button onClick={onSelect}>
            {isActive ? "Recall" : "Send to Battle"}
          </button>
        </div>
      )}
    </div>
  );
}

function App() {
  const [pokemon, setPokemon] = useState(null);
  const [hp, setHp] = useState(0);

  const [team1, setTeam1] = useState([]);
  const [team2, setTeam2] = useState([]);

  const [active1, setActive1] = useState(null);
  const [active2, setActive2] = useState(null);

  const fetchPokemon = async () => {
    try {
      const res = await axios.post("http://localhost:8000/pokemon/", {
        location: "Kanto",
        player_level: 5,
      });
      const data = res.data;

      const poke = {
        id: Date.now(),
        name: data.family,
        image: `http://localhost:8000/images/${data.image}`,
        types: data.types || [],
        hp: data.hp,
        maxHp: data.hp,
        level: data.level || 1,
        moves: data.moves || [],
      };

      setPokemon(poke);
      setHp(poke.hp);
    } catch (err) {
      console.error(err);
    }
  };

  const assignToTeam = (team) => {
    if (!pokemon) return;
    const pokeToAdd = { ...pokemon, hp };
    if (team === 1) setTeam1([...team1, pokeToAdd]);
    else setTeam2([...team2, pokeToAdd]);
    setPokemon(null);
  };

  const removeFromTeam = (team, id) => {
    if (team === 1) {
      setTeam1(team1.filter((p) => p.id !== id));
      if (active1?.id === id) setActive1(null);
    } else {
      setTeam2(team2.filter((p) => p.id !== id));
      if (active2?.id === id) setActive2(null);
    }
  };

  const updateHp = (team, id, newHp) => {
    if (team === 1) {
      setTeam1(team1.map((p) => (p.id === id ? { ...p, hp: newHp } : p)));
      if (active1?.id === id) setActive1({ ...active1, hp: newHp });
    } else {
      setTeam2(team2.map((p) => (p.id === id ? { ...p, hp: newHp } : p)));
      if (active2?.id === id) setActive2({ ...active2, hp: newHp });
    }
  };

  const toggleActive = (team, poke) => {
    if (team === 1) {
      setActive1(active1?.id === poke.id ? null : poke);
    } else {
      setActive2(active2?.id === poke.id ? null : poke);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "row", padding: "1rem" }}>
      {/* Left: controls */}
      <div style={{ flex: 1, textAlign: "center" }}>
        <h1>Pokémon RPG</h1>
        <button onClick={fetchPokemon}>Refresh</button>

        {pokemon && (
          <PokemonCard
            poke={{ ...pokemon, hp }}
            isPreview
            onAssign={assignToTeam}
            onHpChange={(val) => setHp(val)}
          />
        )}
      </div>

      {/* Right: Teams and battle */}
      <div style={{ flex: 2, paddingLeft: "1rem" }}>
        <h2>Team 1</h2>
        <div style={{ display: "flex", overflowX: "auto" }}>
          {team1.map((p) => (
            <PokemonCard
              key={p.id}
              poke={p}
              team={1}
              onRemove={() => removeFromTeam(1, p.id)}
              onHpChange={(val) => updateHp(1, p.id, val)}
              onSelect={() => toggleActive(1, p)}
              isActive={active1?.id === p.id}
            />
          ))}
        </div>

        <h2 style={{ marginTop: "2rem" }}>Team 2</h2>
        <div style={{ display: "flex", overflowX: "auto" }}>
          {team2.map((p) => (
            <PokemonCard
              key={p.id}
              poke={p}
              team={2}
              onRemove={() => removeFromTeam(2, p.id)}
              onHpChange={(val) => updateHp(2, p.id, val)}
              onSelect={() => toggleActive(2, p)}
              isActive={active2?.id === p.id}
            />
          ))}
        </div>

{/* Battle */}
<h2 style={{ marginTop: "2rem" }}>Battle</h2>
<div style={{ display: "flex", justifyContent: "space-around" }}>
  {active1 ? (
    <PokemonCard
      poke={active1}
      team={1}
      isActive
      onHpChange={(val) => updateHp(1, active1.id, val)}  // ✅ allow slider
    />
  ) : (
    <p>No Pokémon from Team 1 in battle</p>
  )}
  {active2 ? (
    <PokemonCard
      poke={active2}
      team={2}
      isActive
      onHpChange={(val) => updateHp(2, active2.id, val)}  // ✅ allow slider
    />
  ) : (
    <p>No Pokémon from Team 2 in battle</p>
  )}
</div>
      </div>
    </div>
  );
}

export default App;