import PokemonCard from "./PokemonCard";

export default function BattleView({ active1, active2, handlers }) {
  return (
    <div>
      <h2>Battle</h2>
      <div style={{ display: "flex", justifyContent: "space-around" }}>
        {active1 ? (
          <PokemonCard poke={active1} team={1} inBattle {...handlers} />
        ) : (
          <p>No Pokémon</p>
        )}
        {active2 ? (
          <PokemonCard poke={active2} team={2} inBattle {...handlers} />
        ) : (
          <p>No Pokémon</p>
        )}
      </div>
    </div>
  );
}
