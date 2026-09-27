"use client";

import React, { useState, useEffect } from "react";
import { KeyRound, Plus, Trash2, Copy, Check, ShieldCheck, AlertCircle } from "lucide-react";
import { getApiKeys, createApiKey, revokeApiKey, ApiKeyItem } from "@/lib/api";

export default function DashboardApiKeysPage() {
  const [keys, setKeys] = useState<ApiKeyItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [keyName, setKeyName] = useState("");
  const [creating, setCreating] = useState(false);
  const [newSecretKey, setNewSecretKey] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadKeys = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getApiKeys();
      setKeys(data);
    } catch (e: any) {
      console.error(e);
      setError(e.message || "Failed to load API keys.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadKeys();
  }, []);

  const handleCreateKey = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!keyName.trim()) return;

    setCreating(true);
    try {
      const created = await createApiKey(keyName);
      if (created.secret_key) {
        setNewSecretKey(created.secret_key);
      }
      setKeyName("");
      await loadKeys();
    } catch (e: any) {
      alert(`Error creating key: ${e.message}`);
    } finally {
      setCreating(false);
    }
  };

  const handleRevoke = async (keyId: string) => {
    if (!confirm("Are you sure you want to revoke this API key? This action is permanent.")) return;
    try {
      await revokeApiKey(keyId);
      await loadKeys();
    } catch (e: any) {
      alert(`Error revoking key: ${e.message}`);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header Card */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-cyan-50 text-cyan-600 flex items-center justify-center">
              <KeyRound className="w-4 h-4" />
            </div>
            <span>Tenant API Key Management</span>
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Generate scoped keys for external e-commerce applications to fetch recommendations and stream behavioral events.
          </p>
        </div>
      </div>

      {/* Secret Key Alert when newly generated */}
      {newSecretKey && (
        <div className="p-5 rounded-2xl bg-emerald-50 border border-emerald-300 text-xs text-emerald-900 space-y-2 shadow-sm">
          <div className="flex items-center space-x-2 font-bold text-sm text-emerald-800">
            <ShieldCheck className="w-5 h-5 text-emerald-600" />
            <span>Save your secret key</span>
          </div>
          <p className="text-[11px] text-emerald-700">
            This secret key is only shown once and cannot be retrieved again. Please store it securely.
          </p>
          <div className="flex items-center space-x-2 bg-white p-3 rounded-xl border border-emerald-300 font-mono text-xs">
            <span className="flex-1 truncate font-bold text-slate-900">{newSecretKey}</span>
            <button
              onClick={() => copyToClipboard(newSecretKey)}
              className="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold flex items-center space-x-1"
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? "Copied" : "Copy"}</span>
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 p-4 rounded-2xl flex items-center justify-between text-xs font-bold">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
          <button
            onClick={loadKeys}
            className="px-3 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded-xl text-xs font-bold transition-all shadow-sm"
          >
            Retry
          </button>
        </div>
      )}

      {/* Create Key Form */}
      <form onSubmit={handleCreateKey} className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-sm flex flex-wrap items-center gap-3">
        <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">Generate New Key:</label>
        <input
          type="text"
          placeholder="e.g. Mobile App Client Key"
          value={keyName}
          onChange={(e) => setKeyName(e.target.value)}
          className="bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 rounded-xl px-3.5 py-2 text-xs focus:outline-none focus:border-cyan-500 w-64 font-medium"
        />
        <button
          type="submit"
          disabled={creating || !keyName.trim()}
          className="px-5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs flex items-center space-x-1.5 shadow-sm transition-all disabled:opacity-50"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>{creating ? "Creating..." : "Create API Key"}</span>
        </button>
      </form>

      {/* API Keys Table */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 uppercase font-mono text-[10px] font-bold tracking-wider">
              <tr>
                <th className="py-3.5 px-5">Key Name</th>
                <th className="py-3.5 px-5">Key Prefix</th>
                <th className="py-3.5 px-5">Permissions / Scopes</th>
                <th className="py-3.5 px-5">Status</th>
                <th className="py-3.5 px-5">Created Date</th>
                <th className="py-3.5 px-5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-slate-400">Loading API keys...</td>
                </tr>
              ) : keys.length > 0 ? (
                keys.map((k) => (
                  <tr key={k.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3.5 px-5 font-bold text-slate-900">{k.name}</td>
                    <td className="py-3.5 px-5 font-mono text-cyan-700 font-bold">
                      {k.key_prefix}&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;
                    </td>
                    <td className="py-3.5 px-5">
                      <div className="flex flex-wrap gap-1">
                        {k.scopes?.map((s) => (
                          <span
                            key={s}
                            className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-slate-100 text-slate-700 border border-slate-200"
                          >
                            {s}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="py-3.5 px-5">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                          !k.is_revoked
                            ? "bg-emerald-100 text-emerald-800 border border-emerald-300"
                            : "bg-rose-100 text-rose-800 border border-rose-300"
                        }`}
                      >
                        {!k.is_revoked ? "ACTIVE" : "REVOKED"}
                      </span>
                    </td>
                    <td className="py-3.5 px-5 text-slate-500 font-medium">
                      {new Date(k.created_at).toLocaleDateString()}
                    </td>
                    <td className="py-3.5 px-5 text-right">
                      {!k.is_revoked && (
                        <button
                          onClick={() => handleRevoke(k.id)}
                          className="px-3 py-1 rounded-xl text-rose-700 hover:bg-rose-50 border border-rose-200 text-xs font-bold transition-colors"
                        >
                          Revoke
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-slate-500">
                    No API keys created yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
