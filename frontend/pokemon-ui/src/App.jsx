import { useState } from "react";
import axios from "axios";

function App() {
  const [pokemon, setPokemon] = useState(null);
  const [showName, setShowName] = useState(false);
  const [hp, setHp] = useState(0);

  // Teams
  const [team1, setTeam1] = useState([]);
  const [team2, setTeam2] = useState([]);

  const fetchPokemon = async () => {
    try {
      const res = await axios.post("http://localhost:8000/pokemon/", {
        location: "Kanto",
        player_level: 5,
      });
      const data = res.data;

      const poke = {
        id: Date.now(), // unique id
        name: data.family,
        image: `http://localhost:8000/images/${data.image}`,
        types: data.types || [],
        hp: data.hp,
        maxHp: data.hp,
        level: data.level || 1,
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

    if (team === 1) {
      setTeam1([...team1, { ...pokemon, hp }]);
    } else {
      setTeam2([...team2, { ...pokemon, hp }]);
    }

    setPokemon(null); // clear central card
  };

  const removeFromTeam = (team, id) => {
    if (team === 1) {
      setTeam1(team1.filter((p) => p.id !== id));
    } else {
      setTeam2(team2.filter((p) => p.id !== id));
    }
  };

  const updateHp = (team, id, newHp) => {
    if (team === 1) {
      setTeam1(
        team1.map((p) => (p.id === id ? { ...p, hp: newHp } : p))
      );
    } else {
      setTeam2(
        team2.map((p) => (p.id === id ? { ...p, hp: newHp } : p))
      );
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
        width: "180px",
        backgroundColor: "#f9f9f9",
        textAlign: "center",
        position: "relative",
      }}
    >
      {/* Remove button */}
      <button
        onClick={() => removeFromTeam(team, poke.id)}
        style={{
          position: "absolute",
          top: "4px",
          right: "4px",
          background: "red",
          color: "white",
          border: "none",
          borderRadius: "50%",
          cursor: "pointer",
          width: "24px",
          height: "24px",
        }}
      >
        ✕
      </button>

      {/* Level badge */}
      <div
        style={{
          position: "absolute",
          top: "4px",
          left: "4px",
          backgroundColor: "#4CAF50",
          color: "white",
          padding: "2px 6px",
          borderRadius: "12px",
          fontSize: "0.8rem",
          fontWeight: "bold",
        }}
      >
        Lv {poke.level}
      </div>

      <h4>{poke.name}</h4>
      <img
        src={poke.image}
        alt={poke.name}
        width="100"
        style={{
          border: "2px solid #ccc",
          borderRadius: "8px",
          marginTop: "0.5rem",
        }}
      />
      <div style={{ marginTop: "0.5rem" }}>
        {poke.types.map((t, i) => (
          <img
            key={i}
            src={`http://localhost:8000/images/types/${t}.png`}
            alt={t}
            title={t}
            width="25"
            style={{ margin: "0 2px" }}
          />
        ))}
      </div>
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
    </div>
  );

  return (
    <div style={{ display: "flex", flexDirection: "row", padding: "1rem" }}>
      {/* Left side: central controls */}
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
              width: "250px",
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
            <button onClick={() => setShowName(!showName)}>
              {showName ? "Hide Name" : "Show Name"}
            </button>
            {showName && <h2>{pokemon.name}</h2>}

            <img
              src={pokemon.image}
              alt={pokemon.name}
              width="150"
              style={{
                border: "2px solid #ccc",
                borderRadius: "8px",
                marginTop: "1rem",
              }}
            />

            <div style={{ marginTop: "0.5rem" }}>
              {pokemon.types.map((t, i) => (
                <img
                  key={i}
                  src={`http://localhost:8000/images/types/${t}.png`}
                  alt={t}
                  title={t}
                  width="40"
                  style={{ margin: "0 5px" }}
                />
              ))}
            </div>

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
        <div style={{ display: "flex", flexDirection: "row" }}>
          {team1.map((p) => renderCard(p, 1))}
        </div>

        <h2 style={{ marginTop: "2rem" }}>Team 2</h2>
        <div style={{ display: "flex", flexDirection: "row" }}>
          {team2.map((p) => renderCard(p, 2))}
        </div>
      </div>
    </div>
  );
}

export default App;
