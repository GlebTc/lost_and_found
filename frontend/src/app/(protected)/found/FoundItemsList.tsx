// components/found/FoundItemsList.tsx
import FoundItemCard from './FoundItemCard';
import { Item } from './types';

const FoundItemsList = ({ items }: { items: Item[] }) => {
  return (
    <div className='flex flex-wrap gap-6 py-8'>
      {items && items.map((item) => (
        <FoundItemCard
          key={item.id}
          title={item.title}
          description={item.description}
          date_found={item.date_reported_turned_in}
          location={`Level ${item.level ?? '?'} - Dept ${item.department ?? '?'}`}
        />
      ))}
    </div>
  );
};

export default FoundItemsList;
