import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Trash2, Eye, Calendar, Plus } from 'lucide-react';
import { getTimetables, deleteTimetable } from '../services/api';

export default function Dashboard() {
    const [timetables, setTimetables] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadTimetables();
    }, []);

    const loadTimetables = async () => {
        try {
            const { data } = await getTimetables();
            setTimetables(data);
        } catch (error) {
            console.error("Failed to load timetables", error);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (name) => {
        if (confirm(`Delete timetable "${name}"?`)) {
            await deleteTimetable(name);
            loadTimetables();
        }
    };

    if (loading) return <div className="p-8 text-center">Loading...</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-900">Your Timetables</h1>
                <Link to="/new" className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 flex items-center">
                    <Plus className="h-5 w-5 mr-1" />
                    Create New
                </Link>
            </div>

            {timetables.length === 0 ? (
                <div className="text-center py-12 bg-white rounded-lg shadow">
                    <Calendar className="mx-auto h-12 w-12 text-gray-400" />
                    <h3 className="mt-2 text-sm font-medium text-gray-900">No timetables</h3>
                    <p className="mt-1 text-sm text-gray-500">Get started by creating a new one.</p>
                </div>
            ) : (
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                    {timetables.map((t) => (
                        <div key={t.id} className="bg-white overflow-hidden shadow rounded-lg border border-gray-100 hover:shadow-md transition-shadow">
                            <div className="px-4 py-5 sm:p-6">
                                <div className="flex items-center">
                                    <div className="flex-shrink-0 bg-indigo-100 rounded-md p-3">
                                        <Calendar className="h-6 w-6 text-indigo-600" />
                                    </div>
                                    <div className="ml-4 w-0 flex-1">
                                        <h3 className="text-lg font-medium text-gray-900 truncate">{t.name}</h3>
                                        <p className="text-sm text-gray-500">Created: {new Date(t.created_at).toLocaleDateString()}</p>
                                    </div>
                                </div>
                            </div>
                            <div className="bg-gray-50 px-4 py-4 sm:px-6 flex justify-end space-x-2">
                                <Link to={`/view/${t.name}`} className="text-indigo-600 hover:text-indigo-900 flex items-center px-3 py-1 bg-white border border-gray-200 rounded-md shadow-sm text-sm">
                                    <Eye className="h-4 w-4 mr-1" /> View
                                </Link>
                                <button onClick={() => handleDelete(t.name)} className="text-red-600 hover:text-red-900 flex items-center px-3 py-1 bg-white border border-gray-200 rounded-md shadow-sm text-sm">
                                    <Trash2 className="h-4 w-4 mr-1" /> Delete
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
