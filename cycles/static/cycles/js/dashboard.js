function formatMinutesToTime(totalMinutes) {
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
    const ampm = hours >= 12 ? 'PM' : 'AM';
    const formattedHours = hours % 12 === 0 ? 12 : hours % 12;
    const formattedMinutes = minutes < 10 ? '0' + minutes : minutes;
    return `${formattedHours}:${formattedMinutes} ${ampm}`;
}

function formatMMDDToMonthDay(mmdd) {
    const month = Math.floor(mmdd / 100);
    const day = mmdd % 100;
    const date = new Date(2000, month - 1, day);
    return date.toLocaleDateString(undefined, { month: 'long', day: 'numeric' });
}

function formatMinutesToDuration(totalMinutes) {
    if (totalMinutes < 0) return 'N/A';
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
    return `${hours}h ${minutes}m remaining`;
}

function formatRecommendations(recommendations) {
    if (!recommendations) return '';
    try {
        const data = typeof recommendations === 'string' ? JSON.parse(recommendations) : recommendations;
        let html = '';
        for (const [category, recs] of Object.entries(data)) {
            html += `<h6 class="font-semibold text-sm mt-2">${category.charAt(0).toUpperCase() + category.slice(1)}</h6>`;
            html += '<ul class="list-disc pl-5 space-y-1">';
            if (Array.isArray(recs)) {
                for (const rec of recs) {
                    html += `<li>${rec}</li>`;
                }
            } else {
                html += `<li>${recs}</li>`;
            }
            html += '</ul>';
        }
        return html;
    } catch {
        const items = typeof recommendations === 'string' ? recommendations.split(';').filter(r => r.trim()) : [];
        if (items.length === 0) return recommendations;
        let html = '<ul class="list-disc pl-5 space-y-1">';
        for (const rec of items) {
            html += `<li>${rec.trim()}</li>`;
        }
        html += '</ul>';
        return html;
    }
}

function updateCurrentCycleInfoFromContext() {
    const ctx = window.djangoContext;
    if (!ctx) return;

    const dailyPeriod = ctx.daily_cycle_period;

    function updateCycleCard(prefix, period, daysIntoPeriod, periodDuration) {
        const currentCycleEl = document.getElementById(`current-${prefix}-cycle`);
        const progressEl = document.getElementById(`${prefix}-progress`);
        const timeRemainingEl = document.getElementById(`${prefix}-time-remaining`);

        if (period && period.period_name) {
            let range = `${period.start_value} - ${period.end_value}`;
            if (prefix === 'daily') range = `${formatMinutesToTime(period.start_value)} - ${formatMinutesToTime(period.end_value)}`;
            else if (prefix === 'soul') range = `${formatMMDDToMonthDay(period.start_value)} - ${formatMMDDToMonthDay(period.end_value)}`;

            if (currentCycleEl) currentCycleEl.textContent = `${period.period_name} (${range})`;

            if (prefix === 'daily') {
                const now = new Date();
                const curMin = now.getHours() * 60 + now.getMinutes();
                let pStart = period.start_value, pEnd = period.end_value;
                let dur = pEnd - pStart;
                if (pStart > pEnd) dur = (24 * 60 - pStart) + pEnd;
                let prog = ((curMin - pStart) / dur) * 100;
                if (pStart > pEnd && curMin < pStart) prog = ((24 * 60 - pStart + curMin) / dur) * 100;
                prog = Math.max(0, Math.min(100, prog));
                if (progressEl) progressEl.style.width = `${prog}%`;
                if (timeRemainingEl) {
                    let rem = pEnd - curMin;
                    if (pStart > pEnd && curMin >= pStart) rem = pEnd - curMin + (24 * 60 - pStart);
                    else if (pStart > pEnd && curMin < pStart) rem = pEnd - curMin;
                    if (rem < 0) rem += 24 * 60;
                    timeRemainingEl.textContent = formatMinutesToDuration(rem);
                }
            }
        }

        if (daysIntoPeriod && periodDuration) {
            const d = Number(daysIntoPeriod);
            const dur = Number(periodDuration);
            if (!isNaN(d) && !isNaN(dur) && dur > 0) {
                const prog = (d / dur) * 100;
                if (progressEl) progressEl.style.width = `${Math.min(100, prog)}%`;
                if (timeRemainingEl) timeRemainingEl.textContent = `${dur - d} days remaining`;
            }
        }
    }

    updateCycleCard('daily', dailyPeriod);
    updateCycleCard('yearly', null, ctx.yearly_days_into_period, ctx.yearly_period_duration);
    updateCycleCard('business', null, ctx.business_days_into_period, ctx.business_period_duration);
    updateCycleCard('health', null, ctx.health_days_into_period, ctx.health_period_duration);
    updateCycleCard('reincarnation', null, ctx.reincarnation_days_into_period, ctx.reincarnation_period_duration);
}
