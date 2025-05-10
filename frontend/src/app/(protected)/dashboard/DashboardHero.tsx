import React from 'react';

const DashboardHero = () => {
  return (
    <section className='bg-gradient-to-b from-[var(--background)] to-[var(--main-color)] py-16 md:py-24 rounded-xl mt-12'>
      <div className='max-w-6xl mx-auto px-4 md:px-6'>
        <div className='grid gap-6 lg:grid-cols-2 lg:gap-12 items-center'>
          <div className='space-y-6'>
            <div className='space-y-4'>
              <h1 className='text-3xl md:text-5xl font-bold tracking-tight text-[hsl(var(--secondary))]'>
                Lost Something? Found Something?
              </h1>
              <p className='text-gray-700 dark:text-gray-300 md:text-xl'>
                Hamilton Health Sciences' Lost and Found platform connects people
                who've lost items with those who've found them. Our system makes
                it easy to report and search for lost or found items.
              </p>

              {/* Button Group */}
              <div className='grid grid-cols-2 gap-3'>
                <a href='/lost'>
                  <button className='w-full px-6 py-3 rounded-lg bg-cyan-700 hover:bg-cyan-600 text-white font-semibold cursor-pointer transition duration-[var(--duration)]'>
                    Report Lost Item
                  </button>
                </a>
                <a href='/found'>
                  <button className='w-full px-6 py-3 rounded-lg bg-cyan-900 hover:bg-cyan-800 text-white font-semibold cursor-pointer transition duration-[var(--duration)]'>
                    Report Found Item
                  </button>
                </a>
                <a href='/lost-items'>
                  <button className='w-full px-6 py-3 rounded-lg bg-none hover:bg-gray-200 text-[var(--main-color)] border border-[var(--main-color)] font-semibold cursor-pointer transition duration-[var(--duration)]'>
                    View Lost Items
                  </button>
                </a>
                <a href='/found-items'>
                  <button className='w-full px-6 py-3 rounded-lg bg-none hover:bg-gray-200 text-[var(--main-color)] border border-[var(--main-color)] font-semibold cursor-pointer transition duration-[var(--duration)]'>
                    View Found Items
                  </button>
                </a>
              </div>
            </div>
          </div>

          <div className='lg:ml-auto'>
            <div className='aspect-video overflow-hidden rounded-xl bg-gray-200 dark:bg-gray-700'>
              <img
                src='https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=1080'
                alt='Lost and Found Items'
                className='object-cover w-full h-full'
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default DashboardHero;
