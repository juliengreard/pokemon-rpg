import { useState } from "react";
import axios from "axios";

function App() {
  const [pokemon, setPokemon] = useState(null);
  const [showName, setShowName] = useState(false);
  const [hp, setHp] = useState(0);

  // Teams
  const [team1, setTeam1] = useState([]);
  const [team2, setTeam2] = useState([]);

  // 🔧 tweak these if you want them bigger/smaller
  const TYPE_SIZE_MAIN = 72; // main card type icon width (logo + text)
  const TYPE_SIZE_CARD = 48; // team card type icon width

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
        moves: data.moves || [], // ensure moves exists
      };

      setPokemon(poke);
      setHp(poke.hp);
      setShowName(false);
    } catch (err) {
      console.error(err);
    }
  };

  const assignToTeam = (team) => {
    if (!pokemon) return;
    const pokeToAdd = { ...pokemon, hp, moves: pokemon.moves || [] };
    if (team === 1) setTeam1([...team1, pokeToAdd]);
    else setTeam2([...team2, pokeToAdd]);
    setPokemon(null);
  };

  const removeFromTeam = (team, id) => {
    if (team === 1) setTeam1(team1.filter((p) => p.id !== id));
    else setTeam2(team2.filter((p) => p.id !== id));
  };

  const updateHp = (team, id, newHp) => {
    if (team === 1) {
      setTeam1(team1.map((p) => (p.id === id ? { ...p, hp: newHp } : p)));
    } else {
      setTeam2(team2.map((p) => (p.id === id ? { ...p, hp: newHp } : p)));
    }
  };

  const renderCard = (poke, team) => (
    <div
      key={poke.id}
      style={{
        margin: "0.5rem",
        padding: "0.5rem",
        border: "2px solid #ddd",
        borderRadius: "8px",
        width: "200px",
        backgroundColor: "#f9f9f9",
        textAlign: "center",
        position: "relative",
      }}
    >
      {/* X button */}
      <button
        onClick={() => removeFromTeam(team, poke.id)}
        title="Remove"
        aria-label="Remove Pokémon from team"
        style={{
          position: "absolute",
          top: "6px",
          right: "6px",
          width: "28px",
          height: "28px",
          padding: 0,
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
          lineHeight: 1,
        }}
      >
        ×
      </button>

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

      <h4 style={{ marginTop: "0.75rem" }}>{poke.name}</h4>
      <img
        src={poke.image}
        alt={poke.name}
        width="120"
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
            title={t}
            width={TYPE_SIZE_CARD}
            style={{ objectFit: "contain", height: "auto" }}
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
          onChange={(e) => updateHp(team, poke.id, Number(e.target.value))}
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
                    src={`http://localhost:8000/images/types/${move.type}.png`}
                    alt={move.type}
                    width={32}
                    style={{ objectFit: "contain", height: "auto" }}
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
          <p style={{ fontStyle: "italic", color: "#888" }}>No moves available</p>
        )}
      </div>
    </div>
  );

  return (
    <div style={{ display: "flex", flexDirection: "row", padding: "1rem" }}>
      {/* Left: central controls */}
      <div style={{ flex: 1, textAlign: "center" }}>
        <h1>Pokémon RPG</h1>
        <button onClick={fetchPokemon}>Refresh</button>

        {pokemon && (
          <div
            style={{
              marginTop: "2rem",
              padding: "1rem",
              border: "2px solid #ddd",
              borderRadius: "8px",
              display: "inline-block",
              width: "280px",
              backgroundColor: "#f9f9f9",
              position: "relative",
            }}
          >
            {/* Level badge */}
            <div
              style={{
                position: "absolute",
                top: "8px",
                left: "8px",
                backgroundColor: "#4CAF50",
                color: "white",
                padding: "4px 10px",
                borderRadius: "12px",
                fontSize: "1rem",
                fontWeight: "bold",
              }}
            >
              Lv {pokemon.level}
            </div>

            {/* Name toggle */}
            <button
              onClick={() => setShowName(!showName)}
              style={{ marginBottom: "0.5rem" }}
            >
              {showName ? "Hide Name" : "Show Name"}
            </button>
            {showName && <h2 style={{ margin: "0.5rem 0" }}>{pokemon.name}</h2>}

            <img
              src={pokemon.image}
              alt={pokemon.name}
              width="170"
              style={{
                border: "2px solid #ccc",
                borderRadius: "8px",
                marginTop: "0.5rem",
              }}
            />

            {/* Types */}
            <div
              style={{
                marginTop: "0.75rem",
                display: "flex",
                gap: "8px",
                justifyContent: "center",
                flexWrap: "wrap",
              }}
            >
              {pokemon.types.map((t, i) => (
                <img
                  key={i}
                  src={`http://localhost:8000/images/types/${t}.png`}
                  alt={t}
                  title={t}
                  width={TYPE_SIZE_MAIN}
                  style={{ objectFit: "contain", height: "auto" }}
                />
              ))}
            </div>

            {/* HP slider */}
            <div style={{ marginTop: "1rem" }}>
              <label>HP: {hp}</label>
              <input
                type="range"
                min="0"
                max={pokemon.hp}
                value={hp}
                onChange={(e) => setHp(Number(e.target.value))}
                style={{ width: "100%", accentColor: "green" }}
              />
            </div>

            {/* Moves */}
            <div style={{ marginTop: "1rem", textAlign: "left" }}>
              <h4 style={{ marginBottom: "0.5rem" }}>Moves:</h4>
              {pokemon.moves.length > 0 ? (
                <ul style={{ paddingLeft: "1rem" }}>
                  {pokemon.moves.map((move, idx) => (
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
                          src={`http://localhost:8000/images/types/${move.type}.png`}
                          alt={move.type}
                          width={32}
                          style={{ objectFit: "contain", height: "auto" }}
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

            {/* Assign buttons */}
            <div style={{ marginTop: "1rem" }}>
              <button onClick={() => assignToTeam(1)}>Assign to Team 1</button>
              <button
                onClick={() => assignToTeam(2)}
                style={{ marginLeft: "0.5rem" }}
              >
                Assign to Team 2
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Right side: Teams */}
      <div style={{ flex: 1 }}>
        <h2>Team 1</h2>
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            flexWrap: "nowrap",
            overflowX: "auto",
          }}
        >
          {team1.map((p) => renderCard(p, 1))}
        </div>

        <h2 style={{ marginTop: "2rem" }}>Team 2</h2>
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            flexWrap: "nowrap",
            overflowX: "auto",
          }}
        >
          {team2.map((p) => renderCard(p, 2))}
        </div>
      </div>
    </div>
  );
}

export default App;
