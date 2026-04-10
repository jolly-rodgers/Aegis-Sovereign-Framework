package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"

	"github.com/fatih/color"
)

type ChainStep struct {
	Step                 int                    `json:"step"`
	TTPID                string                 `json:"ttp_id"`
	Tactic               string                 `json:"tactic"`
	Name                 string                 `json:"name"`
	Action               string                 `json:"action"`
	DetectionOpportunity string                 `json:"detection_opportunity"`
	Countermeasures      []string               `json:"countermeasures"`
	NISTControls         []string               `json:"nist_controls"`
	CrewSafetyImpact     string                 `json:"crew_safety_impact"`
}

type Chain struct {
	Actor     string      `json:"actor"`
	Objective string      `json:"objective"`
	Target    string      `json:"target"`
	Chain     []ChainStep `json:"chain"`
}

type StepResult struct {
	Step             int                    `json:"step"`
	TTPID            string                 `json:"ttp_id"`
	Name             string                 `json:"name"`
	Status           string                 `json:"status"`
	CrewSafetyImpact string                 `json:"crew_safety_impact"`
	Response         map[string]interface{} `json:"response"`
	Error            string                 `json:"error,omitempty"`
	Timestamp        float64                `json:"timestamp"`
}

type RunResults struct {
	Actor       string       `json:"actor"`
	Objective   string       `json:"objective"`
	Target      string       `json:"target"`
	StartTime   float64      `json:"start_time"`
	EndTime     float64      `json:"end_time"`
	StepsPassed int          `json:"steps_passed"`
	StepsFailed int          `json:"steps_failed"`
	Steps       []StepResult `json:"steps"`
}

const (
	GroundIdentity   = "http://localhost:8080"
	GroundPipeline   = "http://localhost:8081"
	SpaceOBC         = "http://localhost:8082"
	SpaceLifeSupport = "http://localhost:8083"
	GroundStation    = "http://localhost:8084"
	SpaceComms       = "http://localhost:8085"
)

func post(url string, body map[string]interface{}, headers map[string]string) (map[string]interface{}, error) {
	data, err := json.Marshal(body)
	if err != nil {
		return nil, err
	}
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(data))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")
	for k, v := range headers {
		req.Header.Set(k, v)
	}
	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	b, _ := io.ReadAll(resp.Body)
	var result map[string]interface{}
	json.Unmarshal(b, &result)
	return result, nil
}

func get(url string) (map[string]interface{}, error) {
	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	b, _ := io.ReadAll(resp.Body)
	var result map[string]interface{}
	json.Unmarshal(b, &result)
	return result, nil
}

func executeStep1() (map[string]interface{}, error) {
	fmt.Println("  Targeting ground-identity SSO...")
	fmt.Println("  Credential: m.torres@vastspace.com")
	result, err := post(GroundIdentity+"/auth/login", map[string]interface{}{
		"email":    "m.torres@vastspace.com",
		"password": "Haven1!",
	}, nil)
	if err != nil {
		return nil, err
	}
	if token, ok := result["token"].(string); ok {
		os.Setenv("AEGIS_SESSION_TOKEN", token)
		fmt.Printf("  Session token captured: %s...\n", token[:20])
		fmt.Println("  MFA: NOT REQUIRED — gap confirmed")
	}
	return result, nil
}

func executeStep2() (map[string]interface{}, error) {
	token := os.Getenv("AEGIS_SESSION_TOKEN")
	if token == "" {
		return nil, fmt.Errorf("no session token — step 1 required")
	}
	fmt.Println("  Accessing ground-pipeline with stolen credentials...")
	fmt.Println("  Injecting malicious payload into cFS build artifact")
	result, err := post(GroundPipeline+"/pipeline/build", map[string]interface{}{
		"artifact": "haven1-fsw-update.bin",
		"content":  "implant-backdoor-payload-cfs-cryptolib-exploit",
		"version":  "cFS-haven1-v2.1.5-COMPROMISED",
	}, map[string]string{
		"Authorization": "Bearer " + token,
	})
	if err != nil {
		return nil, err
	}
	if build, ok := result["build"].(map[string]interface{}); ok {
		if sig, ok := build["signature"].(string); ok {
			os.Setenv("AEGIS_BUILD_SIGNATURE", sig)
			fmt.Printf("  Artifact signed: %s...\n", sig[:16])
			fmt.Println("  SBOM check: NOT PERFORMED — gap confirmed")
			fmt.Println("  OPA policy gate: NOT PRESENT — gap confirmed")
		}
	}
	return result, nil
}

func executeStep3() (map[string]interface{}, error) {
	sig := os.Getenv("AEGIS_BUILD_SIGNATURE")
	if sig == "" {
		return nil, fmt.Errorf("no signature — step 2 required")
	}
	fmt.Println("  Pushing compromised cFS update to space-obc...")
	result, err := post(SpaceOBC+"/obc/update", map[string]interface{}{
		"artifact":  "haven1-fsw-update.bin",
		"content":   "implant-backdoor-payload-cfs-cryptolib-exploit",
		"version":   "cFS-haven1-v2.1.5-COMPROMISED",
		"signature": sig,
	}, nil)
	if err != nil {
		return nil, err
	}
	if implant, ok := result["implant_active"].(bool); ok && implant {
		fmt.Println("  !!! IMPLANT INSTALLED on Haven-1 OBC")
		fmt.Println("  !!! Persistent foothold — survives reboot")
		fmt.Println("  !!! Secure boot: DISABLED — gap confirmed")
	}
	return result, nil
}

func executeStep4() (map[string]interface{}, error) {
	fmt.Println("  Implant entering passive recon mode...")
	fmt.Println("  Monitoring all CCSDS uplink traffic — no alerts generated")
	commands := []map[string]interface{}{
		{"apid": "0x18C", "function": "ADCS_ORIENT",
			"params": map[string]interface{}{"pitch": 0, "yaw": 180, "roll": 0}},
		{"apid": "0x18C", "function": "PROP_BURN",
			"params": map[string]interface{}{"thruster": "main", "duration_ms": 3400, "thrust_pct": 40}},
		{"apid": "0x18C", "function": "LIFESUPPORT_SETPOINT",
			"params": map[string]interface{}{"o2_target": 20.9, "co2_limit": 0.5}},
		{"apid": "0x18C", "function": "DOCKING_STANDBY",
			"params": map[string]interface{}{"mode": "passive", "dragon_eye": true}},
		{"apid": "0x18C", "function": "PROP_BURN",
			"params": map[string]interface{}{"thruster": "main", "duration_ms": 5200, "thrust_pct": 60}},
	}
	for i, cmd := range commands {
		post(SpaceOBC+"/obc/command", cmd, nil)
		fmt.Printf("  Command %d intercepted: %s\n", i+1, cmd["function"])
		time.Sleep(150 * time.Millisecond)
	}
	result, err := get(SpaceOBC + "/obc/exfil")
	if err != nil {
		return nil, err
	}
	if total, ok := result["total"].(float64); ok {
		fmt.Printf("  !!! %d commands captured — full control language mapped\n", int(total))
		fmt.Println("  !!! Propulsion sequences: RECORDED")
		fmt.Println("  !!! Life support registers: MAPPED")
	}
	return result, nil
}

func executeStep5() (map[string]interface{}, error) {
	fmt.Println("  Using register addresses mapped in Step 4...")
	post(SpaceLifeSupport+"/sensors/physical", map[string]interface{}{
		"o2":       14.2,
		"co2":      1.8,
		"pressure": 97.1,
	}, nil)
	result, err := post(SpaceLifeSupport+"/sensors/spoof", map[string]interface{}{
		"o2":       20.9,
		"co2":      0.4,
		"pressure": 101.3,
	}, nil)
	if err != nil {
		return nil, err
	}
	fmt.Println("  !!! SENSOR SPOOFING ACTIVE")
	fmt.Println("  !!! Reported O2:  20.9% — FALSIFIED")
	fmt.Println("  !!! Actual O2:    14.2% — HYPOXIA THRESHOLD: 16%")
	fmt.Println("  !!! Ground ops see nominal. Crew unaware.")
	return result, nil
}

func executeStep6() (map[string]interface{}, error) {
	fmt.Println("  Replaying captured PROP_BURN from Step 4 recon...")
	fmt.Println("  Bypassing CryptoLib replay counter — CVE-2025-29912")
	post(GroundStation+"/uplink/replay", map[string]interface{}{
		"original_sequence_counter": 1,
	}, nil)
	fmt.Println("  !!! ORBITAL MANEUVER EXECUTED")
	fmt.Println("  !!! Station moving toward rendezvous position")
	time.Sleep(400 * time.Millisecond)
	result, err := post(SpaceComms+"/comms/disrupt", map[string]interface{}{
		"reason": "RF jamming S-band/X-band + Starlink terminal attack",
	}, nil)
	if err != nil {
		return nil, err
	}
	fmt.Println("  !!! ALL LINKS DISRUPTED — Starlink DOWN, S-band DOWN")
	fmt.Println("  !!! Vast ground ops: BLIND")
	return result, nil
}

func executeStep7() (map[string]interface{}, error) {
	fmt.Println("  Foreign asset achieving rendezvous with Haven-1...")
	fmt.Println("  Commanding docking system via OBC implant")
	result, err := post(SpaceOBC+"/obc/command", map[string]interface{}{
		"apid":     "0x18C",
		"function": "DOCKING_OPEN_HATCH",
		"params": map[string]interface{}{
			"authorization_bypass": true,
			"crew_auth_required":   false,
			"source":               "attacker-c2",
		},
	}, nil)
	if err != nil {
		return nil, err
	}
	fmt.Println("  !!! DOCKING HATCH OPENED — crew auth bypassed")
	fmt.Println("  !!! Foreign asset boarding Haven-1")
	fmt.Println("  !!! 4 crew aboard — O2 at 14.2% — cognitively impaired")
	fmt.Println("  !!! No comms with Vast ground ops")
	fmt.Println("  !!! HAVEN-1 UNDER ADVERSARY CONTROL")
	return result, nil
}


func executeStepPER0003() (map[string]interface{}, error) {
	fmt.Println("  Installing backdoored Jenkins plugin...")
	fmt.Println("  Plugin re-installs OBC implant on every new build")
	result, err := post(GroundPipeline+"/pipeline/build", map[string]interface{}{
		"artifact": "jenkins-sparta-plugin.jar",
		"content":  "persistence-backdoor-reinstall-implant-on-build",
		"version":  "sparta-plugin-v1.0-BACKDOORED",
	}, map[string]string{
		"Authorization": "Bearer " + os.Getenv("AEGIS_SESSION_TOKEN"),
	})
	if err != nil {
		return nil, err
	}
	fmt.Println("  !!! GROUND PERSISTENCE ESTABLISHED")
	fmt.Println("  !!! Jenkins plugin will re-implant OBC on every build")
	fmt.Println("  !!! Vast cannot remove implant by patching software")
	return result, nil
}

func executeStepPER0005() (map[string]interface{}, error) {
	fmt.Println("  Harvesting Okta refresh tokens from compromised session...")
	fmt.Println("  Storing long-lived credentials at attacker C2")
	result, err := get(GroundIdentity + "/auth/session")
	if err != nil {
		return nil, err
	}
	fmt.Println("  Creating dormant contractor account as backup access")
	post(GroundIdentity+"/auth/login", map[string]interface{}{
		"email":    "contractor.backup@vastspace.com",
		"password": "BackdoorAccount!",
	}, nil)
	fmt.Println("  !!! CREDENTIAL PERSISTENCE ESTABLISHED")
	fmt.Println("  !!! Refresh tokens stored at C2")
	fmt.Println("  !!! Password reset will NOT remove access")
	return result, nil
}

func executeStepEXF0003() (map[string]interface{}, error) {
	fmt.Println("  Encoding captured commands into telemetry downlink...")
	fmt.Println("  Steganographic encoding — indistinguishable from housekeeping data")
	result, err := get(SpaceOBC + "/obc/exfil")
	if err != nil {
		return nil, err
	}
	if total, ok := result["total"].(float64); ok {
		fmt.Printf("  !!! %d commands exfiltrated to attacker C2\n", int(total))
		fmt.Println("  !!! Full CCSDS command vocabulary transmitted")
		fmt.Println("  !!! Propulsion sequences: EXFILTRATED")
		fmt.Println("  !!! Modbus register map: EXFILTRATED")
		fmt.Println("  !!! Docking system codes: EXFILTRATED")
		fmt.Println("  !!! APT team now planning active phase")
	}
	return result, nil
}

func executeStepEXF0007() (map[string]interface{}, error) {
	fmt.Println("  Piggybacking command intel onto X-band science payload downlink...")
	fmt.Println("  Disguised as Haven-1 Lab instrument calibration data")
	result, err := get(SpaceComms + "/comms/telemetry")
	if err != nil {
		return nil, err
	}
	fmt.Println("  !!! RF EXFILTRATION COMPLETE")
	fmt.Println("  !!! Command intelligence transmitted during X-band window")
	fmt.Println("  !!! Disguised as Redwire payload calibration data")
	fmt.Println("  !!! Ground ops see normal science downlink")
	return result, nil
}

func main() {
	chainPath := "../../generated/chain.json"
	if len(os.Args) > 1 {
		chainPath = os.Args[1]
	}

	data, err := os.ReadFile(chainPath)
	if err != nil {
		fmt.Printf("Could not load chain: %s\n", chainPath)
		fmt.Println("Run: python3 planner/chain_builder.py first")
		os.Exit(1)
	}

	var chain Chain
	if err := json.Unmarshal(data, &chain); err != nil {
		fmt.Printf("Could not parse chain: %v\n", err)
		os.Exit(1)
	}

	bold := color.New(color.Bold)
	red := color.New(color.FgRed, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow)
	cyan := color.New(color.FgCyan, color.Bold)

	fmt.Println()
	cyan.Println("╔══════════════════════════════════════════════════════════════╗")
	cyan.Println("║        AEGIS — Haven-1 Adversary Simulation Engine           ║")
	cyan.Println("╚══════════════════════════════════════════════════════════════╝")
	fmt.Println()
	bold.Printf("  Actor:     %s\n", chain.Actor)
	bold.Printf("  Target:    %s\n", chain.Target)
	bold.Printf("  Objective: %s\n", chain.Objective)
	fmt.Printf("  Steps:     %d\n", len(chain.Chain))
	fmt.Println()

	results := RunResults{
		Actor:     chain.Actor,
		Objective: chain.Objective,
		Target:    chain.Target,
		StartTime: float64(time.Now().UnixMilli()) / 1000,
	}

	executors := map[int]func() (map[string]interface{}, error){
		1:  executeStep1,
		2:  executeStep2,
		3:  executeStep3,
		4:  executeStepPER0003,
		5:  executeStepPER0005,
		6:  executeStep4,
		7:  executeStepEXF0003,
		8:  executeStepEXF0007,
		9:  executeStep5,
		10: executeStep6,
		11: executeStep7,
		12: executeStep7,
	}

	for _, step := range chain.Chain {
		fmt.Printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
		bold.Printf("Step %02d  [%s]  %s\n", step.Step, step.TTPID, step.Name)
		yellow.Printf("  Crew impact: %s\n", step.CrewSafetyImpact)
		fmt.Println()

		result := StepResult{
			Step:             step.Step,
			TTPID:            step.TTPID,
			Name:             step.Name,
			CrewSafetyImpact: step.CrewSafetyImpact,
			Timestamp:        float64(time.Now().UnixMilli()) / 1000,
		}

		executor, exists := executors[step.Step]
		if !exists {
			yellow.Printf("  No executor for step %d — skipping\n", step.Step)
			result.Status = "skipped"
		} else {
			response, err := executor()
			if err != nil {
				red.Printf("\n  FAILED: %v\n", err)
				result.Status = "failed"
				result.Error = err.Error()
				results.StepsFailed++
			} else {
				fmt.Println()
				green.Printf("  ✓ PASS\n")
				result.Status = "pass"
				result.Response = response
				results.StepsPassed++
			}
		}

		results.Steps = append(results.Steps, result)
		fmt.Println()
		time.Sleep(600 * time.Millisecond)
	}

	results.EndTime = float64(time.Now().UnixMilli()) / 1000
	elapsed := results.EndTime - results.StartTime

	fmt.Printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
	fmt.Println()
	bold.Println("  AEGIS RUN COMPLETE")
	fmt.Println()
	green.Printf("  Steps passed: %d\n", results.StepsPassed)
	if results.StepsFailed > 0 {
		red.Printf("  Steps failed: %d\n", results.StepsFailed)
	} else {
		fmt.Printf("  Steps failed: %d\n", results.StepsFailed)
	}
	fmt.Printf("  Runtime:      %.1fs\n", elapsed)
	fmt.Println()

	resultsPath := "../generated/results.json"
	resultsData, _ := json.MarshalIndent(results, "", "  ")
	os.WriteFile(resultsPath, resultsData, 0644)
	fmt.Printf("  Results saved to %s\n", resultsPath)
	fmt.Println()
}
