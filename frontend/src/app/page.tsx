export default function Home() {
  return (
    <div className='text-black p-20'>
      <section
        className='py-16 md:py-24'
        style={{
          backgroundImage: `linear-gradient(to bottom, hsl(var(--background)), hsl(var(--accent)))`,
        }}
      >
        <h1>Home Page</h1>
        <p>Welcome to the Lost and Found system.</p>
      </section>
    </div>
  );
}
