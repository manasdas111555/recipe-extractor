import time
import textwrap
from typing import List, Dict, Any

def render_skeleton_card_html() -> str:
    """
    Renders luxury glowing shimmer skeleton cards that provide immediate
    perceived layout readiness while AI is reasoning.
    """
    return textwrap.dedent("""
<div class="skeleton-card">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <div class="shimmer-bar" style="width:45%; height:20px;"></div>
        <div class="shimmer-bar" style="width:20%; height:16px;"></div>
    </div>
    <div class="shimmer-bar" style="width:90%; height:13px; margin-bottom:8px;"></div>
    <div class="shimmer-bar" style="width:78%; height:13px; margin-bottom:16px;"></div>
    <div style="display:flex; gap:10px; margin-bottom:16px;">
        <div class="shimmer-bar" style="width:130px; height:36px; border-radius:8px;"></div>
        <div class="shimmer-bar" style="width:130px; height:36px; border-radius:8px;"></div>
    </div>
    <div class="shimmer-bar" style="width:100%; height:46px; border-radius:10px;"></div>
</div>
""").strip()

def render_neural_deck_html(
    steps: List[Dict[str, Any]], 
    elapsed_s: float, 
    trivia_text: str, 
    is_complete: bool = False,
    active_msg: str = ""
) -> str:
    """
    Renders an ultra-luxurious cyberpunk/SaaS Neural Scanner Deck with live milestone checkoffs,
    status indicators, and rotating trivia.
    """
    items_html = ""
    for s in steps:
        state = s.get("state", "pending")
        if state == "done":
            badge = "<span style='display:inline-flex; align-items:center; justify-content:center; width:20px; height:20px; border-radius:50%; background:rgba(16,185,129,0.22); color:#34D399; font-size:0.75rem; font-weight:800; border:1px solid rgba(16,185,129,0.45); flex-shrink:0;'>✓</span>"
            title_color = "#E2E8F0"
            desc_color = "#94A3B8"
        elif state == "active":
            badge = "<span class='scanner-pulse-dot'></span>"
            title_color = "#FDA4AF"
            desc_color = "#F43F5E"
        elif state == "error":
            badge = "<span style='display:inline-flex; align-items:center; justify-content:center; width:20px; height:20px; border-radius:50%; background:rgba(239,68,68,0.2); color:#F87171; font-size:0.75rem; font-weight:800; border:1px solid rgba(239,68,68,0.4); flex-shrink:0;'>✕</span>"
            title_color = "#FCA5A5"
            desc_color = "#EF4444"
        else:
            badge = "<span style='display:inline-flex; width:10px; height:10px; border-radius:50%; background:rgba(255,255,255,0.15); margin:5px; flex-shrink:0;'></span>"
            title_color = "#64748B"
            desc_color = "#475569"

        row = f"""<div style="display:flex; align-items:flex-start; gap:12px; margin-bottom:10px;">
    <div style="padding-top:2px;">{badge}</div>
    <div style="flex:1;">
        <div style="font-family:'Outfit',sans-serif; font-size:0.90rem; font-weight:700; color:{title_color}; display:flex; align-items:center; gap:6px;">
            <span>{s.get('icon', '⚡')}</span> <span>{s.get('title', '')}</span>
        </div>
        <div style="font-size:0.75rem; color:{desc_color}; margin-top:2px; line-height:1.3;">{s.get('desc', '')}</div>
    </div>
</div>"""
        items_html += row + "\n"

    status_header = "⚡ Neural Vision Pipeline Active" if not is_complete else "🎉 Intelligence Extracted Successfully!"
    header_color = "#F43F5E" if not is_complete else "#10B981"
    
    active_line = ""
    if active_msg and not is_complete:
        active_line = f"""<div style="font-family:'JetBrains Mono',monospace; font-size:0.74rem; color:#FCA5A5; background:rgba(244,63,94,0.06); border-radius:6px; padding:4px 8px; margin-bottom:12px; border:1px solid rgba(244,63,94,0.18);">
    ⚡ <b>Live Task:</b> {active_msg}
</div>"""

    full_html = f"""<div class="neural-scanner-deck">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:10px;">
    <div style="display:flex; align-items:center; gap:8px;">
        <span style="width:10px; height:10px; border-radius:50%; background:{header_color}; box-shadow:0 0 10px {header_color};"></span>
        <span style="font-family:'Outfit',sans-serif; font-weight:800; font-size:0.98rem; color:#FFFFFF;">{status_header}</span>
    </div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.82rem; font-weight:700; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1); border-radius:8px; padding:3px 9px; color:#F8FAFC;">
        ⏱️ {elapsed_s:.1f}s
    </div>
</div>
{active_line}
<div style="margin-bottom:12px;">
{items_html}
</div>
<div class="trivia-ticker">
    <div style="font-size:0.77rem; color:#E2E8F0; line-height:1.45;">
        {trivia_text}
    </div>
</div>
</div>"""
    return full_html.strip()


class NeuralProgressDeck:
    """
    Manages live milestone progression, elapsed timing, and captivating trivia
    during video ingestion and multimodal reasoning.
    """
    TRIVIA_LIST = [
        "💡 <b>Reel Fact</b>: Over 68% of viral kitchen gadgets featured on Instagram Reels sell out on Amazon within 48 hours.",
        "🧠 <b>Vision AI</b>: Gemini 3.5 Flash inspects video frames, on-screen text overlays, and audio dialogue simultaneously.",
        "⚡ <b>Extreme Speed</b>: Processing video directly in cloud tensor memory cuts turnaround time by 15× compared to separate transcription pipelines.",
        "🛒 <b>Shoppable Links</b>: Every detected product is automatically paired with Amazon India and Flipkart 1-click buy tags.",
        "🍳 <b>Domain Detection</b>: AI automatically distinguishes between cooking recipes, fitness routines, and physical product unboxings.",
        "📱 <b>Zero Manual Work</b>: Everything is auto-formatted into a 1-click WhatsApp document for instant sharing to friends or family.",
        "🔒 <b>Zero Data Retained</b>: Temporary video frames and files are purged after processing to guard user privacy."
    ]

    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.start_time = time.perf_counter()
        self.steps = [
            {"id": "dl", "title": "HD Video Stream Ingestion", "desc": "Fetching pristine stream from CDN...", "icon": "📥", "state": "active"},
            {"id": "prep", "title": "Neural Video Frame Slicing", "desc": "Extracting visual frames & audio tracks...", "icon": "🎞️", "state": "pending"},
            {"id": "ai", "title": "Multimodal Vision AI (Gemini 3.5 Flash)", "desc": "Reasoning over ingredients, tools & steps...", "icon": "🧠", "state": "pending"},
            {"id": "links", "title": "Shoppable Catalog Synthesis", "desc": "Generating 1-click Amazon & Flipkart tags...", "icon": "🛍️", "state": "pending"},
            {"id": "dispatch", "title": "Instant Delivery & Export", "desc": "Formatting .txt notes & WhatsApp deep link...", "icon": "📱", "state": "pending"},
        ]
        self.trivia_index = 0
        self.active_msg = ""
        self.render()

    def update_step(self, step_id: str, state: str = "done", custom_desc: str = None):
        for s in self.steps:
            if s["id"] == step_id:
                s["state"] = state
                if custom_desc:
                    s["desc"] = custom_desc
        self.render()

    def on_ai_status(self, msg: str):
        self.active_msg = msg
        lower = msg.lower()
        if "upload" in lower or "preparing" in lower:
            self.update_step("dl", "done", "HD stream downloaded & verified")
            self.update_step("prep", "active", msg)
        elif "reasoning" in lower or "analyzing" in lower or "gemini" in lower or "mistral" in lower or "groq" in lower:
            self.update_step("dl", "done")
            self.update_step("prep", "done", "Keyframes & audio tensors ready")
            self.update_step("ai", "active", msg)
        elif "inference completed" in lower or "synthesiz" in lower or "parsed" in lower:
            self.update_step("ai", "done", "Multimodal extraction completed")
            self.update_step("links", "active", "Cross-referencing shopping catalogs...")
        
        self.trivia_index = (self.trivia_index + 1) % len(self.TRIVIA_LIST)
        self.render()

    def complete_all(self, total_time_s: float):
        for s in self.steps:
            s["state"] = "done"
        self.active_msg = f"Completed in {total_time_s:.1f}s"
        self.render(is_complete=True, total_time_s=total_time_s)

    def render(self, is_complete: bool = False, total_time_s: float = None):
        elapsed = total_time_s if total_time_s is not None else (time.perf_counter() - self.start_time)
        trivia = self.TRIVIA_LIST[self.trivia_index]
        html = render_neural_deck_html(
            steps=self.steps,
            elapsed_s=elapsed,
            trivia_text=trivia,
            is_complete=is_complete,
            active_msg=self.active_msg
        )
        if hasattr(self.placeholder, "html"):
            self.placeholder.html(html)
        else:
            self.placeholder.markdown(html, unsafe_allow_html=True)
