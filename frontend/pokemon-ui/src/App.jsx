import { useState } from "react";
import axios from "axios";
import { useEffect, useRef } from "react";

function App() {
  const [pokemon, setPokemon] = useState(null);
  const [showName, setShowName] = useState(false);
  const [hp, setHp] = useState(0);

  // Teams & active Pokémon in battle
  const [team1, setTeam1] = useState([]);
  const [team2, setTeam2] = useState([]);
  const [active1, setActive1] = useState(null);
  const [active2, setActive2] = useState(null);

  const TYPE_SIZE_MAIN = 72;
  const TYPE_SIZE_CARD = 48;

  // Fetch a wild Pokémon
  const fetchPokemon = async () => {
    try {
      const res = await axios.post("http://localhost:8000/pokemon/", {
        location: "Kanto",
        player_level: 5,
      });
      const data = res.data;

      const poke = {
        id: Date.now(),
        family: data.family,
        image: `http://localhost:8000/images/${data.image}`,
        types: data.types || [],
        hp: data.hp,
        level: data.level || 1,
        moves: data.moves || [],
      };

      setPokemon(poke);
      setHp(poke.hp);
      setShowName(false);
    } catch (err) {
      console.error(err);
    }
  };

  // --- helpers ---
  const updatePokemonHp = (team, id, newHp) => {
    if (team === 1) {
      setTeam1(team1.map((p) => (p.id === id ? { ...p, hp: newHp } : p)));
      if (active1?.id === id) setActive1({ ...active1, hp: newHp });
    } else {
      setTeam2(team2.map((p) => (p.id === id ? { ...p, hp: newHp } : p)));
      if (active2?.id === id) setActive2({ ...active2, hp: newHp });
    }
  };

// Call whenever active Pokémon change

const lastBattlePairRef = useRef({ id1: null, id2: null });

useEffect(() => {
  if (!active1 || !active2) return;

  // Only call if this pair is different from last call
  if (
    lastBattlePairRef.current.id1 === active1.id &&
    lastBattlePairRef.current.id2 === active2.id
  ) {
    return; // same pair, skip
  }

  lastBattlePairRef.current = { id1: active1.id, id2: active2.id };

  // Call the backend
  updateBattleMoves();
}, [active1, active2]);


const updateBattleMoves = async () => {
  console.log("Updating battle moves...");
  console.log("Active1:", active1);
  console.log("Active2:", active2);
  if (!active1 || !active2) return;

  try {
    const res = await axios.post("http://localhost:8000/battle/update_moves", {
      pokemon1: active1,
      pokemon2: active2,
    });

    const { pokemon1: updated1, pokemon2: updated2 } = res.data;

    // Only update the active Pokémon, NOT the team
    setActive1((prev) => ({ ...prev, moves: updated1.moves || [] }));
    setActive2((prev) => ({ ...prev, moves: updated2.moves || [] }));
  } catch (err) {
    console.error("Failed to update battle moves:", err);
  }
};

  // --- team handling ---
  const assignToTeam = (team) => {
    if (!pokemon) return;
    const pokeToAdd = { ...pokemon, hp, moves: pokemon.moves || [] };
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

const setActivePokemon = (team, poke) => {
  if (team === 1) setActive1(poke);
  else setActive2(poke);
};


  // --- render cards ---
  const renderCard = (poke, team, selectable = true, inBattle = false) => (
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
      {/* Remove button */}
      {!inBattle && (
        <button
          onClick={() => removeFromTeam(team, poke.id)}
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
          <img key={i} src={`http://localhost:8000/images/types/${t}.png`} alt={t} width={TYPE_SIZE_CARD} />
        ))}
      </div>

      {/* HP */}
      <div style={{ marginTop: "0.5rem" }}>
        <label>HP: {poke.hp}</label>
        {inBattle ? (
          <div style={{ background: "#ddd", height: "8px", borderRadius: "4px", overflow: "hidden" }}>
            <div
              style={{
                width: `${(poke.hp / poke.maxHp) * 100}%`,
                background: "green",
                height: "100%",
              }}
            />
          </div>
        ) : (
          <input
            type="range"
            min="0"
            max={poke.maxHp}
            value={poke.hp}
            onChange={(e) => updatePokemonHp(team, poke.id, Number(e.target.value))}
            style={{ width: "100%", accentColor: "green" }}
          />
        )}
      </div>

      {/* Moves */}
      <div style={{ marginTop: "1rem", textAlign: "left" }}>
        <h4 style={{ marginBottom: "0.5rem" }}>Moves:</h4>
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
                  <strong>{m.name}</strong> {m.power && `(Power: ${m.power})`}
                </div>
                <small>{m.description}</small>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ fontStyle: "italic", color: "#888" }}>No moves</p>
        )}
      </div>

      {/* Send to battle / Recall */}
      {!inBattle && selectable && (
        <div style={{ marginTop: "0.5rem" }}>
          <button onClick={() => setActivePokemon(team, poke)}>Send to Battle</button>
        </div>
      )}

      {inBattle && (
        <div style={{ marginTop: "0.5rem" }}>
          <button
            onClick={() => (team === 1 ? setActive1(null) : setActive2(null))}
            style={{ backgroundColor: "#f44336", color: "white", padding: "4px 8px", border: "none", borderRadius: "4px" }}
          >
            Recall
          </button>
        </div>
      )}
    </div>
  );

  return (
    <div style={{ display: "flex", flexDirection: "row", padding: "1rem" }}>
      {/* Left: wild Pokémon */}
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
              background: "#f9f9f9",
              position: "relative",
            }}
          >
            {/* Level */}
            <div
              style={{
                position: "absolute",
                top: "8px",
                left: "8px",
                background: "#4CAF50",
                color: "white",
                padding: "4px 10px",
                borderRadius: "12px",
                fontWeight: "bold",
              }}
            >
              Lv {pokemon.level}
            </div>

            <button onClick={() => setShowName(!showName)}>
              {showName ? "Hide Name" : "Show Name"}
            </button>
            {showName && <h2>{pokemon.family}</h2>}

            <img src={pokemon.image} alt={pokemon.family} width="170" />

            {/* Types */}
            <div style={{ marginTop: "0.75rem", display: "flex", gap: "8px", justifyContent: "center" }}>
              {pokemon.types.map((t, i) => (
                <img
                  key={i}
                  src={`http://localhost:8000/images/types/${t}.png`}
                  alt={t}
                  width={TYPE_SIZE_MAIN}
                />
              ))}
            </div>

            {/* HP */}
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
                  {pokemon.moves.map((m, idx) => (
                    <li key={idx} style={{ marginBottom: "0.5rem" }}>
                      <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                        <img
                          src={`http://localhost:8000/images/types/move_${m.type}.png`}
                          alt={m.type}
                          width={24}
                        />
                        <strong>{m.name}</strong> {m.power && `(Power: ${m.power})`}
                      </div>
                      <small>{m.description}</small>
                    </li>
                  ))}
                </ul>
              ) : (
                <p style={{ fontStyle: "italic", color: "#888" }}>No moves</p>
              )}
            </div>

            <div style={{ marginTop: "1rem" }}>
              <button onClick={() => assignToTeam(1)}>Assign to Team 1</button>
              <button onClick={() => assignToTeam(2)} style={{ marginLeft: "0.5rem" }}>
                Assign to Team 2
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Right: Teams & Battle */}
      <div style={{ flex: 1 }}>
        <h2>Team 1</h2>
        <div style={{ display: "flex", overflowX: "auto" }}>
          {team1.map((p) => renderCard(p, 1))}
        </div>

        <h2 style={{ marginTop: "2rem" }}>Team 2</h2>
        <div style={{ display: "flex", overflowX: "auto" }}>
          {team2.map((p) => renderCard(p, 2))}
        </div>

        <h2 style={{ marginTop: "2rem" }}>Battle</h2>
        <div style={{ display: "flex", justifyContent: "space-around" }}>
          {active1 ? renderCard(active1, 1, false, true) : <p>No Pokémon</p>}
          {active2 ? renderCard(active2, 2, false, true) : <p>No Pokémon</p>}
        </div>
      </div>
    </div>
  );
}

export default App;
