import React from "react";

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  const handlePrevious = () => {
    if (currentPage > 0) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages - 1) {
      onPageChange(currentPage + 1);
    }
  };

  return (
    <div className="pagination">
      <button onClick={handlePrevious} disabled={currentPage === 0}>Previous</button>
      <span>Page {currentPage + 1} of {totalPages}</span>
      <button onClick={handleNext} disabled={currentPage === totalPages - 1}>Next</button>
    </div>
  );
};
export default Pagination;