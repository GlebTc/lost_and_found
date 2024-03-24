import Link from "next/link";

const NavMenuDesktop = ({
  isAdmin,
  isMember,
}: {
  isAdmin: boolean;
  isMember: boolean;
}) => {
  return (
    <div className="flex space-x-4">
      <Link href="/" className="text-white hover:text-gray-300">
        Home
      </Link>
      {(isMember || isAdmin) && (
        <Link href="/lost" className="text-white hover:text-gray-300">
          Lost Items
        </Link>
      )}
      {(isMember || isAdmin) && (
        <Link href="/found" className="text-white hover:text-gray-300">
          Found Items
        </Link>
      )}
      {isAdmin && (
        <Link href="/admin" className="text-white hover:text-gray-300">
          Admin Panel
        </Link>
      )}
    </div>
  );
};

export default NavMenuDesktop;