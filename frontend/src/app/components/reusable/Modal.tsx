interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

const Modal = ({ isOpen, onClose, children }: ModalProps) => {
  return (
    <>
      {isOpen && (
        <div className="fixed inset-0 flex justify-center items-center z-50">
          <div className="fixed inset-0 bg-black opacity-75"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-lg shadow-lg w-3/4">
            {children}
          </div>
        </div>
      )}
    </>
  );
};

export default Modal;