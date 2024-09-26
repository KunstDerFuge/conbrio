import {Document, Page} from '@react-pdf/renderer'

export default function PDFReader(props) {
  return (
    <>
      <Document file={`data:application/pdf;base64,${props.pdf}`}>
        <Page pageNumber={1} />
      </Document>
    </>
  )
}