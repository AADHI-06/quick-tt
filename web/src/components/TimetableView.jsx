import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Printer } from 'lucide-react';
import { getTimetable } from '../services/api';

export default function TimetableView() {
    const { name } = useParams();
    const [timetable, setTimetable] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadTimetable();
    }, [name]);

    const loadTimetable = async () => {
        try {
            const { data } = await getTimetable(name);
            setTimetable(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="p-8 text-center">Loading...</div>;
    if (!timetable) return <div className="p-8 text-center">Timetable not found</div>;

    // Transform entries into grid
    // entries: [{class_name, period_index, subject}, ...]
    // We need distinct classes and max periods.
    const classes = [...new Set(timetable.entries.map(e => e.class_name))].sort();
    const maxPeriod = Math.max(...timetable.entries.map(e => e.period_index)) + 1;
    const periods = Array.from({ length: maxPeriod }, (_, i) => i);

    const grid = {};
    timetable.entries.forEach(e => {
        if (!grid[e.class_name]) grid[e.class_name] = {};
        grid[e.class_name][e.period_index] = e.subject;
    });

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between no-print">
                <div className="flex items-center">
                    <Link to="/" className="text-indigo-600 hover:text-indigo-800 mr-4">
                        <ArrowLeft className="h-6 w-6" />
                    </Link>
                    <h1 className="text-3xl font-bold text-gray-900">{timetable.name}</h1>
                </div>
                <button onClick={() => window.print()} className="bg-gray-100 p-2 rounded hover:bg-gray-200">
                    <Printer className="h-6 w-6 text-gray-600" />
                </button>
            </div>

            <div className="bg-white shadow overflow-hidden rounded-lg print:shadow-none">
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200 text-center">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Period
                                </th>
                                {classes.map(cls => (
                                    <th key={cls} className="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        {cls}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {periods.map(p => (
                                <tr key={p} className={p % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900 border-r">
                                        {p + 1}
                                    </td>
                                    {classes.map(cls => (
                                        <td key={`${cls}-${p}`} className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                            {grid[cls]?.[p] || "-"}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
