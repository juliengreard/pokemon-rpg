import { useState } from "react";
import axios from "axios";

function App() {
  const [pokemon, setPokemon] = useState(null);
  const [showName, setShowName] = useState(false);
  const [hp, setHp] = useState(0);

  const fetchPokemon = async () => {
    try {
      const res = await axios.post("http://localhost:8000/pokemon/", {
        location: "Kanto",
        player_level: 5,
      });
      const data = res.data;

      const poke = {
        name: data.family,
        image: `http://localhost:8000/images/${data.image}`,
        types: data.types || [], // array of type names
        hp: data.hp,
      };

      setPokemon(poke);
      setHp(poke.hp); // initialize slider
      setShowName(false);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "2rem" }}>
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
          }}
        >
          {/* Show name toggle */}
          <button onClick={() => setShowName(!showName)}>
            {showName ? "Hide Name" : "Show Name"}
          </button>
          {showName && <h2>{pokemon.name}</h2>}

          {/* Pokémon image */}
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

          {/* Type images */}
          <div style={{ marginTop: "0.5rem" }}>
            {pokemon.types.map((t, i) => (
              <img
                key={i}
                src={`http://localhost:8000/images/types/${t}.png`} // <-- place your type icons in backend /images/types/
                alt={t}
                title={t}
                width="80"
                style={{ margin: "0 1px" }}
              />
            ))}
          </div>

          {/* HP Slider */}
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
        </div>
      )}
    </div>
  );
}

export default App;
