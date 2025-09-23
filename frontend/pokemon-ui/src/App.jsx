import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import TeamView from "./components/TeamView";
import BattleView from "./components/BattleView";
import PokemonCard from "./components/PokemonCard";

function App() {
  const [pokemon, setPokemon] = useState(null);
  const [hp, setHp] = useState(0);

  const [team1, setTeam1] = useState([]);
  const [team2, setTeam2] = useState([]);
  const [active1, setActive1] = useState(null);
  const [active2, setActive2] = useState(null);

  const TYPE_SIZE_MAIN = 72;

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
      console.log("Fetched wild Pokémon:", poke);
    } catch (err) {
      console.error("fetchPokemon error:", err);
    }
  };

  // load team endpoint
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
      setTeam1((prev) => prev.map((p) => (p.id === id ? { ...p, hp: newHp } : p)));
      if (active1?.id === id) setActive1((prev) => ({ ...prev, hp: newHp }));
    } else {
      setTeam2((prev) => prev.map((p) => (p.id === id ? { ...p, hp: newHp } : p)));
      if (active2?.id === id) setActive2((prev) => ({ ...prev, hp: newHp }));
    }
  };

  // assign to team (this is the function you reported missing)
  const assignToTeam = (team) => {
    if (!pokemon) return;
    const pokeToAdd = { ...pokemon, hp, maxHp: pokemon.hp, moves: pokemon.moves || [] };
    if (team === 1) setTeam1((prev) => [...prev, pokeToAdd]);
    else setTeam2((prev) => [...prev, pokeToAdd]);
    setPokemon(null);
  };

  // remove from team
  const removeFromTeam = (team, id) => {
    if (team === 1) {
      setTeam1((prev) => prev.filter((p) => p.id !== id));
      if (active1?.id === id) setActive1(null);
    } else {
      setTeam2((prev) => prev.filter((p) => p.id !== id));
      if (active2?.id === id) setActive2(null);
    }
  };

const setActivePokemon = (team, poke) => {
  if (team === 1) {
    setActive1(poke ? { ...poke, moves: [] } : null);
  } else {
    setActive2(poke ? { ...poke, moves: [] } : null);
  }
};
  const recallActive = (team) => {
    if (team === 1) setActive1(null);
    else setActive2(null);
  };

  // --- status handlers (sync team array & active) ---
  const affectStatus = (team, status, disableText) => {
    const opponentActive = team === 1 ? active2 : active1;
    if (!opponentActive) return;

    if (team === 1) {
      setActive2((prev) => (prev ? { ...prev, status, status_effect_deactivation_chance: disableText } : null));
      setTeam2((prev) => prev.map((p) => (p.id === opponentActive.id ? { ...p, status, status_effect_deactivation_chance: disableText } : p)));
    } else {
      setActive1((prev) => (prev ? { ...prev, status, status_effect_deactivation_chance: disableText } : null));
      setTeam1((prev) => prev.map((p) => (p.id === opponentActive.id ? { ...p, status, status_effect_deactivation_chance: disableText } : p)));
    }
  };

  const disableStatus = (team, status) => {
    const currentPoke = team === 1 ? active1 : active2;
    if (!currentPoke) return;
    if (team === 1) {
      setActive1((prev) => (prev ? { ...prev, status: null } : null));
      setTeam1((prev) => prev.map((p) => (p.id === currentPoke.id ? { ...p, status: null } : p)));
    } else {
      setActive2((prev) => (prev ? { ...prev, status: null } : null));
      setTeam2((prev) => prev.map((p) => (p.id === currentPoke.id ? { ...p, status: null } : p)));
    }
  };

  // --- battle move update (call once when active pair changes) ---
  const lastBattlePairRef = useRef({ id1: null, id2: null });

  useEffect(() => {
    if (!active1 || !active2) {
      if (!active1) lastBattlePairRef.current.id1 = null;
      if (!active2) lastBattlePairRef.current.id2 = null;
      return;
    }

    if (lastBattlePairRef.current.id1 === active1.id && lastBattlePairRef.current.id2 === active2.id) {
      return;
    }

    lastBattlePairRef.current = { id1: active1.id, id2: active2.id };
    updateBattleMoves();
    // eslint-disable-next-line react-hooks/exhaustive-deps
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

  // pack handlers and pass to child components
  const handlers = {
    updatePokemonHp,
    setActivePokemon,
    removeFromTeam,
    affectStatus,
    disableStatus,
    recallActive,
  };

  return (
    <div style={{ display: "flex", flexDirection: "row", padding: 16 }}>
      <div style={{ flex: 1, textAlign: "center" }}>
        <h1>Pokémon RPG</h1>

        {/* Refresh — directly calls fetchPokemon (in-scope) */}
        <button onClick={fetchPokemon}>Refresh</button>

        <div style={{ marginTop: 12 }}>
          <button onClick={() => loadTeam("team1")} style={{ marginLeft: 8 }}>
            Load Team 1
          </button>
          <button onClick={() => loadTeam("team2")} style={{ marginLeft: 8 }}>
            Load Team 2
          </button>
        </div>

{pokemon && (
  <div style={{ display: "inline-block", marginTop: 16 }}>
    <PokemonCard
      poke={{ ...pokemon, hp }}
      team={null}
      selectable={false}
      inBattle={false}
      handlers={{
        updatePokemonHp: (_, __, newHp) => setHp(newHp),
        affectStatus: () => {},
        disableStatus: () => {},
        removeFromTeam: () => {},
        setActivePokemon: () => {}
      }}
    />

    {/* Assign buttons */}
    <div style={{ marginTop: 8, textAlign: "center" }}>
      <button
        onClick={() => assignToTeam(1)}
        style={{
          marginRight: 8,
          backgroundColor: "#4CAF50",
          color: "white",
          padding: "6px 12px",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Add to Team 1
      </button>
      <button
        onClick={() => assignToTeam(2)}
        style={{
          backgroundColor: "#2196F3",
          color: "white",
          padding: "6px 12px",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Add to Team 2
      </button>
    </div>
  </div>
)}


      </div>

      <div style={{ flex: 1 }}>
        <TeamView team={team1} teamNumber={1} handlers={handlers} />
        <TeamView team={team2} teamNumber={2} handlers={handlers} />
        <BattleView active1={active1} active2={active2} handlers={handlers} />
      </div>
    </div>
  );
}

export default App;
