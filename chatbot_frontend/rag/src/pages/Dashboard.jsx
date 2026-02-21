import { useEffect, useState } from "react";
import axios from "axios";

const API = "http://localhost:8000"; // change when deployed

export default function Dashboard() {
  const [files, setFiles] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchDocuments = async () => {
    const res = await axios.get(`${API}/documents`);
    setDocuments(res.data);
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const uploadDocuments = async () => {
    if (files.length === 0) return;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    setLoading(true);

    await axios.post(`${API}/upload`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    setFiles([]);
    fetchDocuments();
    setLoading(false);
  };

  const deleteDocument = async (id) => {
    await axios.delete(`${API}/documents/${id}`);
    fetchDocuments();
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-200 p-8">
      <div className="max-w-5xl mx-auto space-y-10">

        <h1 className="text-3xl font-bold text-white">
          Document Management
        </h1>

        {/* Upload Section */}
        <div className="bg-gray-900 p-6 rounded-2xl border border-gray-800">
          <h2 className="text-xl font-semibold mb-4">Upload Documents</h2>

          <input
            type="file"
            multiple
            onChange={(e) => setFiles(e.target.files)}
            className="mb-4 w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2"
          />

          <button
            onClick={uploadDocuments}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-500 px-6 py-2 rounded-lg font-medium transition"
          >
            {loading ? "Uploading..." : "Upload"}
          </button>
        </div>

        {/* Document List */}
        <div className="bg-gray-900 p-6 rounded-2xl border border-gray-800">
          <h2 className="text-xl font-semibold mb-4">Stored Documents</h2>

          {documents.length === 0 ? (
            <p className="text-gray-500">No documents uploaded yet.</p>
          ) : (
            <div className="space-y-3">
              {documents.map((doc) => (
                <div
                  key={doc.id}
                  className="flex justify-between items-center bg-gray-800 p-4 rounded-xl border border-gray-700"
                >
                  <span>{doc.filename}</span>

                  <button
                    onClick={() => deleteDocument(doc.id)}
                    className="text-red-400 hover:text-red-300"
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

      </div>
    </div>
  );
}