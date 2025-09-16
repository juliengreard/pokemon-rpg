import StatusIcon from "./components/StatusIcons";
import { useState, useEffect, useRef, act } from "react";
import axios from "axios";

function App() {
  const [pokemon, setPokemon] = useState(null);
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
        maxHp: data.hp,
        level: data.level || 1,
        moves: data.moves || [],
        status: null,
      };

      setPokemon(poke);
      setHp(poke.hp);
    } catch (err) {
      console.error(err);
    }
  };

  // Load a team from backend
  const loadTeam = async (team) => {
    try {
      const res = await axios.get(`http://localhost:8000/loadTeam/${team}`);
      const teamData = res.data;

      const loadedTeam = teamData.map((p) => ({
        id: Date.now() + Math.random(),
        family: p.family,
        image: `http://localhost:8000/images/${p.image}`,
        types: p.types || [],
        hp: p.hp,
        maxHp: p.hp,
        level: p.level || 1,
        moves: p.moves || [],
        status: null,
      }));

      if (team === "team1") {
        setTeam1(loadedTeam);
        setActive1(null);
      } else if (team === "team2") {
        setTeam2(loadedTeam);
        setActive2(null);
      }
    } catch (err) {
      console.error(`Failed to load ${team}:`, err);
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

  // Keep track of last battle pair
  const lastBattlePairRef = useRef({ id1: null, id2: null });

  useEffect(() => {
    if (!active1 || !active2) {
      if (!active1) lastBattlePairRef.current.id1 = null;
      if (!active2) lastBattlePairRef.current.id2 = null;
      return;
    }

    if (
      lastBattlePairRef.current.id1 === active1.id &&
      lastBattlePairRef.current.id2 === active2.id
    ) {
      return;
    }

    lastBattlePairRef.current = { id1: active1.id, id2: active2.id };
    updateBattleMoves();
  }, [active1, active2]);

  const updateBattleMoves = async () => {
    if (!active1 || !active2) return;

    const original1 = team1.find((p) => p.id === active1.id);
    const original2 = team2.find((p) => p.id === active2.id);

    if (!original1 || !original2) return;

    try {
      const res = await axios.post("http://localhost:8000/battle/update_moves", {
        pokemon1: original1,
        pokemon2: original2,
      });

      const { pokemon1: updated1, pokemon2: updated2 } = res.data;

      setActive1((prev) => ({ ...prev, moves: updated1.moves || [] }));
      setActive2((prev) => ({ ...prev, moves: updated2.moves || [] }));
    } catch (err) {
      console.error("Failed to update battle moves:", err);
    }
  };

  // --- team handling ---
  const assignToTeam = (team) => {
    if (!pokemon) return;
    const pokeToAdd = { ...pokemon, hp, maxHp: pokemon.hp, moves: pokemon.moves || [] };
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
    if (team === 1) setActive1({ ...poke, moves: [] });
    else setActive2({ ...poke, moves: [] });
  };

  // --- NEW: Sync status with both active and team arrays ---
  const affectStatus = (team, status, disableText) => {
    const opponentActive = team === 1 ? active2 : active1;
    if (!opponentActive) return;

    console.log(`Applying ${status} to ${opponentActive.family}`);

    if (team === 1) {
      setActive2((prev) =>
        prev ? { ...prev, status, status_effect_deactivation_chance: disableText } : null
      );
      setTeam2((prev) =>
        prev.map((p) =>
          p.id === opponentActive.id
            ? { ...p, status, status_effect_deactivation_chance: disableText }
            : p
        )
      );
    } else {
      setActive1((prev) =>
        prev ? { ...prev, status, status_effect_deactivation_chance: disableText } : null
      );
      setTeam1((prev) =>
        prev.map((p) =>
          p.id === opponentActive.id
            ? { ...p, status, status_effect_deactivation_chance: disableText }
            : p
        )
      );
    }
  };

  const disableStatus = (team, status) => {
    console.log(`Request to disable ${status} on team ${team}`);
    const currentPoke = team === 1 ? active1 : active2;
    if (!currentPoke) return;

    console.log(`Disabling ${status} on ${currentPoke.family}`);

    if (team === 1) {
      setActive1((prev) => (prev ? { ...prev, status: null } : null));
      setTeam1((prev) =>
        prev.map((p) => (p.id === currentPoke.id ? { ...p, status: null } : p))
      );
    } else {
      setActive2((prev) => (prev ? { ...prev, status: null } : null));
      setTeam2((prev) =>
        prev.map((p) => (p.id === currentPoke.id ? { ...p, status: null } : p))
      );
    }
  };

  // --- render card ---
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
      <div>
        {poke.status && (
          <StatusIcon
            effect={poke.status}
            text={poke.status_effect_deactivation_chance}
            onClick={() => disableStatus(team, poke.status)}
          />
        )}
      </div>

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
                <small>D: {m.description}</small>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ fontStyle: "italic", color: "#888" }}>No moves</p>
        )}
      </div>

      {!inBattle && selectable && (
        <div style={{ marginTop: "0.5rem" }}>
          <button onClick={() => setActivePokemon(team, poke)}>Send to Battle</button>
        </div>
      )}

      {inBattle && (
        <div style={{ marginTop: "0.5rem" }}>
          <button
            onClick={() => (team === 1 ? setActive1(null) : setActive2(null))}
            style={{
              backgroundColor: "#f44336",
              color: "white",
              padding: "4px 8px",
              border: "none",
              borderRadius: "4px",
            }}
          >
            Recall
          </button>
        </div>
      )}
    </div>
  );

  return (
    <div style={{ display: "flex", flexDirection: "row", padding: "1rem" }}>
      <div style={{ flex: 1, textAlign: "center" }}>
        <h1>Pokémon RPG</h1>
        <button onClick={fetchPokemon}>Refresh</button>
        <button onClick={() => loadTeam("team1")} style={{ marginLeft: "0.5rem" }}>
          Load Team 1
        </button>
        <button onClick={() => loadTeam("team2")} style={{ marginLeft: "0.5rem" }}>
          Load Team 2
        </button>
        {/* wild Pokémon display left unchanged */}
      </div>

      <div style={{ flex: 1 }}>
        <h2>Team 1</h2>
        <div style={{ display: "flex", overflowX: "auto" }}>{team1.map((p) => renderCard(p, 1))}</div>

        <h2 style={{ marginTop: "2rem" }}>Team 2</h2>
        <div style={{ display: "flex", overflowX: "auto" }}>{team2.map((p) => renderCard(p, 2))}</div>

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
