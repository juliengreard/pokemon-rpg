import { useState } from "react";
import axios from "axios";

function App() {
  const [pokemon, setPokemon] = useState(null);

  const fetchPokemon = async () => {
    try {
      const res = await axios.post("http://localhost:8000/pokemon/", {
        location: "Kanto",   // adjust depending on your DB
        player_level: 5
      });
      const data = res.data;

      // // ⚡ your backend returns { family, level, hp }
      // // we’ll also fetch the family details (name, types, number)
      // const familyRes = await axios.get("http://localhost:8000/pokemons");
      // const family = familyRes.data.find((f) => f.family === data.family);

      setPokemon({
        name: data.family,
        image: `http://localhost:8000/images/${data.image}`,
        types: data.types || []
      });
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "2rem" }}>
      <h1>Pokémon RPG</h1>
      <button onClick={fetchPokemon}>Refresh</button>

      {pokemon && (
        <div style={{ marginTop: "2rem" }}>
          <h2>{pokemon.name}</h2>
          <img
            src={pokemon.image}
            alt={pokemon.name}
            width="200"
            style={{ border: "2px solid #ccc", borderRadius: "8px" }}
          />
          <p>Types: {pokemon.types.join(", ")}</p>
        </div>
      )}
    </div>
  );
}

export default App;
