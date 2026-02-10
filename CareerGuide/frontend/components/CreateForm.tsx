export default function CareerForm({ onSubmit }) {
    async function handleSubmit(e) {
      e.preventDefault();
  
      const data = await generateCareer({
        current_role: e.target.current.value,
        target_role: e.target.target.value,
        years_exp: Number(e.target.years.value),
      });
  
      onSubmit(data);
    }
  
    return (
      <form onSubmit={handleSubmit}>
        <input name="current" placeholder="Current Role" />
        <input name="target" placeholder="Target Role" />
        <input name="years" type="number" />
        <button type="submit">Generate Career Plan</button>
      </form>
    );
  }
  