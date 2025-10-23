import { useState, useEffect } from 'react';
import { Plus, Trash2, Globe } from 'lucide-react';
import { blocklistAPI } from '../services/api';

export default function BlocklistManager() {
  const [sites, setSites] = useState([]);
  const [newUrl, setNewUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const presets = [
    { name: 'Social Media', value: 'social_media', icon: '📱' },
    { name: 'News', value: 'news', icon: '📰' },
    { name: 'Entertainment', value: 'entertainment', icon: '🎬' },
  ];

  useEffect(() => {
    fetchSites();
  }, []);

  const fetchSites = async () => {
    try {
      const { data } = await blocklistAPI.getAll();
      setSites(data.sites || []);
    } catch (error) {
      console.error('Error fetching sites:', error);
    }
  };

  const handleAddSite = async (e) => {
    e.preventDefault();
    if (!newUrl.trim()) return;

    setLoading(true);
    try {
      await blocklistAPI.add(newUrl, 'custom');
      setNewUrl('');
      fetchSites();
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to add site');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveSite = async (siteId) => {
    try {
      await blocklistAPI.remove(siteId);
      fetchSites();
    } catch (error) {
      console.error('Error removing site:', error);
    }
  };

  const handleAddPreset = async (category) => {
    setLoading(true);
    try {
      const { data } = await blocklistAPI.addPreset(category);
      alert(`Added ${data.added_count} sites from ${category}`);
      fetchSites();
    } catch (error) {
      alert('Failed to add preset category');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">
        Blocklist Manager
      </h2>

      {/* Add Site Form */}
      <form onSubmit={handleAddSite} className="mb-6">
        <div className="flex gap-3">
          <input
            type="text"
            value={newUrl}
            onChange={(e) => setNewUrl(e.target.value)}
            placeholder="example.com"
            className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-all shadow-md hover:shadow-lg font-semibold flex items-center gap-2 disabled:opacity-50"
          >
            <Plus size={20} />
            Add
          </button>
        </div>
      </form>

      {/* Preset Categories */}
      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-600 mb-3">Quick Add Presets:</h3>
        <div className="grid grid-cols-3 gap-3">
          {presets.map((preset) => (
            <button
              key={preset.value}
              onClick={() => handleAddPreset(preset.value)}
              disabled={loading}
              className="px-4 py-3 bg-gray-100 hover:bg-gray-200 rounded-xl transition-all text-sm font-medium disabled:opacity-50"
            >
              <span className="mr-2">{preset.icon}</span>
              {preset.name}
            </button>
          ))}
        </div>
      </div>

      {/* Sites List */}
      <div className="space-y-2">
        <h3 className="text-sm font-semibold text-gray-600 mb-3">
          Blocked Sites ({sites.length})
        </h3>
        
        {sites.length === 0 ? (
          <div className="text-center py-8 text-gray-400">
            <Globe size={48} className="mx-auto mb-2 opacity-50" />
            <p>No sites blocked yet</p>
          </div>
        ) : (
          <div className="max-h-64 overflow-y-auto space-y-2">
            {sites.map((site) => (
              <div
                key={site.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-all"
              >
                <div className="flex items-center gap-3">
                  <Globe size={16} className="text-gray-400" />
                  <span className="font-medium text-gray-700">{site.url}</span>
                  <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded-full">
                    {site.category}
                  </span>
                </div>
                <button
                  onClick={() => handleRemoveSite(site.id)}
                  className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-all"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
