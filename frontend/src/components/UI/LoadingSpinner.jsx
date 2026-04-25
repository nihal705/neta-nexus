export default function LoadingSpinner() {
  return (
    <div className="flex justify-center items-center py-12">
      <div className="relative">
        <div className="w-12 h-12 border-4 border-primary-teal/20 rounded-full"></div>
        <div className="absolute top-0 left-0 w-12 h-12 border-4 border-primary-teal border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>
  )
}