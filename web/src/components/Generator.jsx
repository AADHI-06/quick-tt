import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Save, Loader, Plus, Minus } from 'lucide-react';
import api from '../services/api';

export default function Generator() {
    const navigate = useNavigate();
    const [periods, setPeriods] = useState(8);
    const [classes, setClasses] = useState([
        { name: "12A", subjects: ["MATH", "PHY", "CHEM", "BIO", "ENG"] },
        { name: "12B", subjects: ["MATH", "PHY", "CHEM", "CS", "ENG"] }
    ]);
    const [generated, setGenerated] = useState(null); // { "12A": [...], ... }
    const [loading, setLoading] = useState(false);
    const [saveName, setSaveName] = useState("");

    const handleGenerate = async () => {
        setLoading(true);
        setGenerated(null);
        try {
            const clsPayload = {};
            classes.forEach(c => {
                // Create a list where each subject appears roughly balanced?
                // For now, let's just create a pool based on the list.
                // Actually the backend expects "Class -> List of ALL subjects to be scheduled".
                // E.g. if periods=8, we need 8 items in the list.
                // Let's assume the user inputs unique subjects and we distribute them.
                // OR we simplify: User inputs "Subject: Count".

                // For SIMPLICITY in this generic UI, let's just repeat the subjects to fill periods for now.
                // Real app would have a counter per subject.

                let expanded = [];
                let i = 0;
                while (expanded.length < periods) {
                    expanded.push(c.subjects[i % c.subjects.length]);
                    i++;
                }
                clsPayload[c.name] = expanded;
            });

            const { data } = await api.post('/generate', {
                periods: parseInt(periods),
                classes: clsPayload
            });
            setGenerated(data);
        } catch (err) {
            alert("Failed to generate: " + (err.response?.data?.detail || err.message));
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        if (!saveName) return alert("Enter a name");
        try {
            await api.post('/timetables', {
                name: saveName,
                periods: parseInt(periods),
                entries: generated
            });
            navigate('/');
        } catch (err) {
            alert("Failed to save: " + err.message);
        }
    };

    const addClass = () => setClasses([...classes, { name: "New Class", subjects: ["SUB1"] }]);

    const updateClass = (idx, field, val) => {
        const newClasses = [...classes];
        newClasses[idx][field] = val;
        setClasses(newClasses);
    };

    const updateSubjects = (idx, val) => {
        // Split by comma
        const subs = val.split(",").map(s => s.trim().toUpperCase()).filter(s => s);
        updateClass(idx, "subjects", subs);
    };

    return (
        <div className="space-y-8 bg-white p-8 rounded-lg shadow">
            <div>
                <h2 className="text-2xl font-bold text-gray-900">Generate Timetable</h2>
                <p className="text-gray-500">Configure your classes and subjects.</p>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Periods per Day</label>
                    <input
                        type="number"
                        value={periods}
                        onChange={(e) => setPeriods(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                    />
                </div>
            </div>

            <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900">Classes</h3>
                {classes.map((cls, idx) => (
                    <div key={idx} className="flex gap-4 items-start border p-4 rounded-md bg-gray-50">
                        <div className="w-1/4">
                            <label className="block text-xs font-medium text-gray-500">Class Name</label>
                            <input
                                value={cls.name}
                                onChange={(e) => updateClass(idx, "name", e.target.value)}
                                className="mt-1 w-full rounded border-gray-300 p-2 shadow-sm"
                            />
                        </div>
                        <div className="flex-1">
                            <label className="block text-xs font-medium text-gray-500">Subjects (comma separated)</label>
                            <input
                                defaultValue={cls.subjects.join(", ")}
                                onBlur={(e) => updateSubjects(idx, e.target.value)}
                                className="mt-1 w-full rounded border-gray-300 p-2 shadow-sm"
                            />
                        </div>
                    </div>
                ))}
                <button onClick={addClass} className="text-sm text-indigo-600 font-medium flex items-center hover:text-indigo-800">
                    <Plus className="h-4 w-4 mr-1" /> Add Class
                </button>
            </div>

            <div className="flex justify-end border-t pt-4">
                <button
                    onClick={handleGenerate}
                    disabled={loading}
                    className="bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50 flex items-center"
                >
                    {loading ? <Loader className="animate-spin h-5 w-5 mr-2" /> : null}
                    Generate Schedule
                </button>
            </div>

            {generated && (
                <div className="mt-8 border-t pt-8">
                    <h3 className="text-xl font-bold mb-4">Preview</h3>
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Class</th>
                                    {Array.from({ length: periods }).map((_, i) => (
                                        <th key={i} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">P{i + 1}</th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {Object.keys(generated).map((cls) => (
                                    <tr key={cls}>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{cls}</td>
                                        {generated[cls].map((sub, i) => (
                                            <td key={i} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{sub}</td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    <div className="mt-6 flex items-end gap-4">
                        <div className="flex-1 max-w-xs">
                            <label className="block text-sm font-medium text-gray-700">Save As</label>
                            <input
                                value={saveName}
                                onChange={(e) => setSaveName(e.target.value)}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
                                placeholder="e.g. Term1_Schedule"
                            />
                        </div>
                        <button onClick={handleSave} className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 flex items-center">
                            <Save className="h-5 w-5 mr-2" /> Save Timetable
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
