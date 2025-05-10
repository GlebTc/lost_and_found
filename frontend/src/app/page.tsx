import Link from 'next/link';

export default function Home() {
  return (
    <div className="text-black p-6 md:p-20">
      <section className="bg-gradient-to-b from-[var(--background)] to-[var(--main-color)] py-16 md:py-24 rounded-xl mt-12 text-center space-y-6">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
          Welcome
        </h1>
        <p className="text-lg md:text-xl text-gray-100 max-w-2xl mx-auto">
          Welcome to the Lost and Found system for Hamilton Health Sciences. Use the button below to access your dashboard.
        </p>
        <Link
          href="/dashboard"
          className="inline-block text-[var(--main-color)] border border-[var(--main-color)] bg-white px-6 py-3 rounded-md font-semibold hover:bg-gray-300 transition duration-[var(--duration)]"
        >
          Go to Dashboard
        </Link>
      </section>
    </div>
  );
}
