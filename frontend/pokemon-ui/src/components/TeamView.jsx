import PokemonCard from "./PokemonCard";

export default function TeamView({ team, teamNumber, handlers }) {
  return (
    <div>
      <h2>Team {teamNumber}</h2>
      <div style={{ display: "flex", overflowX: "auto" }}>
        {team.map((p) => (
          <PokemonCard key={p.id} poke={p} team={teamNumber} {...handlers} />
        ))}
      </div>
    </div>
  );
}
