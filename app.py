5th
        
        <hr style="border: 0; border-top: 1px solid #2d3442; margin: 15px 0;">
        
        <!-- Main Header Logs -->
        <h3 style="font-size: 16px; color: #ffffff; margin-bottom: 5px;">📊 PANKAJ SINGH DESIGN DATA LOGS</h3>
        <div id="live-spot-banner" style="background-color: #2c1a1d; padding: 12px; border-radius: 6px; border: 1px solid #e74c3c; text-align: center; margin-bottom: 15px;">
            <span style="color: #e74c3c; font-weight: bold; font-size: 14px;">NIFTY 50 LIVE SPOT (BEARISH LIVE MODE)</span><br>
            <span id="live-spot-price" style="font-size: 26px; font-weight: bold; color: white;">23148.50</span> &nbsp;&nbsp; 
            <span id="live-spot-change" style="font-size: 16px; color: #e74c3c; font-weight: bold;">-217.95 (-0.93%)</span>
        </div>
        
        <div style="margin-bottom: 20px; font-size: 16px;">
            🎯 <b>EXACT ATM STRIKE (MROUND ENGINE):</b> <span id="atm-strike-val" style="font-weight: bold; color: #f1c40f; font-size: 18px;">23150</span>
        </div>

        <!-- Section 1: Main Option Chain Grid Container -->
        <h3>🖥️ 1. मास्टर ऑप्शन चेन रडार व्यू</h3>
        <div style="display: flex; justify-content: space-between; background-color: #1f242d; border-bottom: 2px solid #2d3442; font-weight: bold; padding: 10px 4px; text-align: center; font-size: 11px; margin-bottom: 5px;">
            <div style="width: 20%;">CE Phase<br>(With Score)</div>
            <div style="width: 24%;">OI Details<br>(VOL / OI PCR)<br>(Chg OI / Chg % Matrix)</div>
            <div style="width: 12%; color: #e67e22;">ST/Strike<br>(PCR)</div>
            <div style="width: 24%;">VOLUME Details<br>(VOLUME / VOL Str)<br>(Chg VOL)</div>
            <div style="width: 20%;">PE Phase<br>(With Score)</div>
        </div>
        <div id="option-chain-rows-container"></div>
        <!-- Section 2.4: 4-Layer Quantum Colony -->
        <hr style="border: 0; border-top: 1px solid #2d3442; margin: 20px 0;">
        <h3>🧠 2.4 4-लेयर पृथक क्वांटम कॉलोनी (+5 / -5 ITM & OTM PCR)</h3>
        <div class="grid-3-col">
            <div style="text-align: left; border-right: 1px dashed #2d3442; padding-right: 10px;">
                <span style="color: #e74c3c; font-weight: bold; font-size: 13px;">🔴 OTM CLUSTER DATA (Left)</span><br>
                <span style="font-size: 10px; color: #7f8c8d;">(Call OTM +5 vs Put OTM -5)</span><br><br>
                <span class="txt-red" id="otm-oi-pcr">🔴 OTM OI PCR: 0.85</span><br>
                <span class="txt-red" id="otm-choi-pcr">🔴 OTM ChgOI PCR: 2.14</span><br>
                <span class="txt-red" id="otm-vol-pcr">🔴 OTM VOL PCR: 1.32</span><br>
                <span class="txt-red" id="otm-chgvol-pcr">🔴 OTM ChgVOL PCR: 1.85</span>
            </div>
            <div style="text-align: center; font-weight: bold; color: #f39c12; font-size: 13px;">
                परत 1-4<br>समरी<br><br><span style="color:#ffffff; font-size:13px;" id="l4-atm-box">ATM 23150</span>
            </div>
            <div style="text-align: left; padding-left: 15px;">
                <span style="color: #3498db; font-weight: bold; font-size: 13px;">🔵 ITM CLUSTER DATA (Right)</span><br>
                <span style="font-size: 10px; color: #7f8c8d;">(Call ITM -5 vs Put ITM +5)</span><br><br>
                <span class="txt-blue" id="itm-oi-pcr">🔵 ITM OI PCR: 1.20</span><br>
                <span class="txt-blue" id="itm-choi-pcr">🔵 ITM ChgOI PCR: 1.45</span><br>
                <span class="txt-blue" id="itm-vol-pcr">🔵 ITM VOL PCR: 0.95</span><br>
                <span class="txt-blue" id="itm-chgvol-pcr">🔵 ITM ChgVOL PCR: 1.12</span>
            </div>
        </div>

        <!-- Section 2.5: 5-Layer Corridor Colony -->
        <hr style="border: 0; border-top: 1px solid #2d3442; margin: 20px 0;">
        <h3>🧠 2.5 5-लेयर पृथक OTM vs ITM (+5 / -5 ITM & OTM PCR)</h3>
        <div class="grid-3-col">
            <div style="text-align: left; border-right: 1px dashed #2d3442; padding-right: 10px;">
                <span style="color: #f39c12; font-weight: bold; font-size: 13px;">⬆️ +5 CORRIDOR DATA (Left)</span><br>
                <span style="font-size: 10px; color: #7f8c8d;">(5 Call OTM vs 5 Put ITM)</span><br><br>
                <span style="color: #f39c12; font-weight: bold;" id="p5-oi-pcr">OI PCR: 0.68</span><br>
                <span style="color: #f39c12; font-weight: bold;" id="p5-choi-pcr">ChgOI PCR: 0.42</span><br>
                <span style="color: #f39c12; font-weight: bold;" id="p5-vol-pcr">VOL PCR: 0.55</span><br>
                <span style="color: #f39c12; font-weight: bold;" id="p5-chgvol-pcr">ChgVOL PCR: 0.38</span>
            </div>
            <div style="text-align: center; font-weight: bold; color: #f39c12; font-size: 13px;">
                परत 1-5<br>मैट्रिक्स<br><br><span style="color:#ffffff; font-size:13px;" id="l5-atm-box">ATM 23150</span>
            </div>
            <div style="text-align: left; padding-left: 15px;">
                <span style="color: #9b59b6; font-weight: bold; font-size: 13px;">⬇️ -5 CORRIDOR DATA (Right)</span><br>
                <span style="font-size: 10px; color: #7f8c8d;">(5 Call ITM vs 5 Put OTM)</span><br><br>
                <span style="color: #9b59b6; font-weight: bold;" id="m5-oi-pcr">OI PCR: 2.34</span><br>
                <span style="color: #9b59b6; font-weight: bold;" id="m5-choi-pcr">ChgOI PCR: 3.12</span><br>
                <span style="color: #9b59b6; font-weight: bold;" id="m5-vol-pcr">VOL PCR: 1.85</span><br>
                <span style="color: #9b59b6; font-weight: bold;" id="m5-chgvol-pcr">ChgVOL PCR: 2.41</span>
            </div>
        </div>

        <!-- Section 3: AI Brain Engine Summary Matrix -->
        <hr style="border: 0; border-top: 1px solid #2d3442; margin: 20px 0;">
        <h3>🤖 3. UNIFIED AI DECISION SCORES (% DISTRIBUTION ENGINE)</h3>
        <div class="grid-3-col">
            <div style="text-align: left; border-right: 1px dashed #2d3442; padding-right: 10px;">
                <span class="txt-red" id="ai-call-score-lbl">AI CALL BUY SCORE: --%</span><br><br>
                <span class="txt-yellow" id="ai-sideways-lbl">🟡 SIDEWAYS SCORE: --%</span>
            </div>
            <div style="text-align: center; font-weight: bold; color: #f39c12; font-size: 13px;">AI<br>BRAIN<br>MATRIX</div>
            <div style="text-align: left; padding-left: 15px;">
                <span class="txt-green" id="ai-put-score-lbl">🔴 AI PUT BUY SCORE: --%</span><br><br>
                <span class="txt-purple" id="ai-trap-lbl">🟣 NO TRADE / TRAP SCORE: --%</span>
            </div>
        </div>

        <!-- Section 4: Expiry Protection Sync Box -->
        <hr style="border: 0; border-top: 1px solid #2d3442; margin: 20px 0;">
        <h3>🍏 4. EXPIRY DAY SPECIAL AI CONFIDENCE ENGINE (IV & THETA SYNC)</h3>
        <div id="expiry-engine-alert-box" style="padding: 14px; border-radius: 6px; font-size: 13px;">
            🔮 Checking Engine Constraints...
        </div>

        <!-- Section 5: Big Players Alert Box -->
        <hr style="border: 0; border-top: 1px solid #2d3442; margin: 20px 0;">
        <h3>🏛️ 5. BIG PLAYERS PANIC, SAFE ZONE & ULTIMATE QUANT ALERTS</h3>
        <div style="background-color: #161b22; padding: 12px; border-radius: 5px; border: 1px solid #e74c3c; color: white; font-size: 13px; line-height: 1.6;">
            <span style="color: #e74c3c; font-weight: bold; font-size: 14px;">🔴 QUANTUM FUSION METRICS ALERT: TAKE PUT BUY ACTIVE (<span id="alert-confidence-lbl">--%</span>)</span><br><br>
            <b>🛑 SELLER PANIC LEVELS (Elasticity Limit):</b><br>
            • Call Seller Panic Zone: <span class="txt-red" id="panic-call-lvl">Above -----</span>. स्विंग सीलिंग पार होने पर कॉल राइटर्स का Unlimited Loss और 💣 Massive Gamma Blast शुरू होगा।<br>
            • Put Seller Panic Zone: <span class="txt-red" id="panic-put-lvl">Below -----</span>. सपोर्ट फ्लोर टूटने पर पुट राइटर्स घबराकर भागेंगे (🔴 OI Fleeing)।<br><br>
            <b>🛡️ INSTITUTIONAL SAFE ZONE (Corridor):</b><br>
            • <span class="txt-blue" id="safe-corridor-lvl">----- — -----</span> के दायरे में बड़े ऑपरेटर्स पूरी तरह सुरक्षित रहकर थीटा डीके वसूलेंगे।
        </div>

        <!-- Section 9: Reversal Levels -->
        <br>
        <h4>⚠️ REVERSAL SATARK ZONE & OHLC LEVELS</h4>
        <div style="display: flex; justify-content: space-between; gap: 15px;">
            <div style="background-color: #1b2a22; padding: 12px; border-radius: 5px; border: 1px solid #2ecc71; width: 50%;">
                <span style="color: #2ecc71; font-weight: bold; font-size: 14px;">🔄 Pull-Back Support Range (Put Side 🟢):</span><br>
                <span style="font-size: 20px; font-weight: bold; color: white;" id="rev-support-range">----- — -----</span><br>
                <span style="font-size: 11px; color: #a3b8cc;" id="rev-support-logic">लॉजिक: Processing Support Floor...</span>
            </div>
            <div style="background-color: #2c1a1d; padding: 12px; border-radius: 5px; border: 1px solid #e74c3c; width: 50%;">
                <span style="color: #e74c3c; font-weight: bold; font-size: 14px;">🛑 Pull-Down Resistance Wall (Call Side 🔴):</span><br>
                <span style="font-size: 20px; font-weight: bold; color: white;" id="rev-resistance-wall">----- — -----</span><br>
                <span style="font-size: 11px; color: #a3b8cc;" id="rev-resistance-logic">लॉजिक: Processing Gamma Wall Limit...</span>
            </div>
        </div>
    </div>
