from gql import gql

UPLOAD_CREATE = gql(
    """
mutation CreateUpload($name: String!, $checksum_sha256: String!, $size: StrInt!) {
  datasetFileUploadCreate(
    name: $name
    checksumSha256: $checksum_sha256
    size: $size
  ) {
    userError {
      field
      message
    }
  }
}
"""
)

UPLOAD_GET = gql(
    """
query GetUpload($name: String!, $part_count: Int) {
  datasetFileUpload(name: $name) {
    numParts
    numUploadedParts
    uploadParts(count: $part_count) {
      bytesEnd
      bytesStart
      url
    }
  }
}
"""
)


FILE_GET = gql(
    """
query GetFile($name: String!) {
  datasetFile(name: $name) {
    status
    size
    name
    downloadUrl
    checksumSha256
  }
}
"""
)

FILES_GET = gql(
    """
query GetFiles {
  datasetFiles {
    status
    size
    name
    downloadUrl
    checksumSha256
  }
}
"""
)
