package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"html/template"
	"io"
	"log"
	"net/http"
	"os"
	"time"
)

var (
	// tpl stores the parsed frontend html template
	tpl *template.Template
)

// Profile represents the message object returned from the backend API.

type Profile struct {
	FirstName      string    `valid:"stringlength(5|20)" json:"first_name" bson:"first_name"`
	LastName       string    `valid:"stringlength(5|20)" json:"last_name" bson:"last_name"`
	LinkedInURL    string    `json:"linkedin_url" bson:"linkedin_url"`
	Avatar         string    `json:"avatar" bson:"avatar"`
	Company        string    `json:"company" bson:"company"`
	Position       string    `json:"position" bson:"position"`
	Connections    string    `json:"connections" bson:"connections"`
	ConnectionDist string    `json:"connection_dist" bson:"connection_dist"`
	TimeInRole     string    `json:"time_in_role" bson:"time_in_role"`
	Activity       string    `json:"activity" bson:"activity"`
	CreatedAt      time.Time `json:"created_at" bson:"created_at"`
}

// main starts a frontend server and connects to the backend.
func main() {
	// LEADOPT_API_ADDR environment variable is provided in leadopt-frontend.deployment.yaml.
	backendAddr := (map[bool]string{true: "localhost:8081", false: os.Getenv("LEADOPT_API_ADDR")})[os.Getenv("LEADOPT_API_ADDR") == ""]

	// PORT environment variable is provided in leadopt-frontend.deployment.yaml.
	port := (map[bool]string{true: "8080", false: os.Getenv("PORT")})[os.Getenv("PORT") == ""]

	// Parse html templates and save them to global variable.
	t, err := template.New("").Funcs(map[string]interface{}{
		"since": sinceDate,
	}).ParseGlob("templates/*.tpl")
	if err != nil {
		log.Fatalf("could not parse templates: %+v", err)
	}
	tpl = t

	// Register http handlers and start listening on port.
	fe := &frontendServer{backendAddr: backendAddr}
	fs := http.FileServer(http.Dir("static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))
	http.HandleFunc("/", fe.homeHandler)
	http.HandleFunc("/post", fe.postHandler)
	log.Printf("frontend server listening on port %s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("server listen error: %+v", err)
	}
}

type frontendServer struct {
	backendAddr string
}

// homeHandler handles GET requests to /.
func (f *frontendServer) homeHandler(w http.ResponseWriter, r *http.Request) {
	log.Printf("received request: %s %s", r.Method, r.URL.Path)
	if r.Method != http.MethodGet {
		http.Error(w, fmt.Sprintf("only GET requests are supported (got %s)", r.Method), http.StatusMethodNotAllowed)
		return
	}
	if r.URL.Path != "/" {
		http.Error(w, "page not found", http.StatusNotFound)
		return
	}

	log.Printf("querying backend for entries: %s", f.backendAddr)
	resp, err := http.Get(fmt.Sprintf("http://%s/api/profile", f.backendAddr))
	if err != nil {
		http.Error(w, fmt.Sprintf("querying backend failed: %+v", err), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		http.Error(w, fmt.Sprintf("failed to read response body: %+v", err), http.StatusInternalServerError)
		return
	}

	if resp.StatusCode != http.StatusOK {
		http.Error(w, fmt.Sprintf("got status code %d from the backend: %s", resp.StatusCode, string(body)), http.StatusInternalServerError)
		return
	}

	log.Printf("parsing backend response into json")
	var v []Profile
	if err := json.Unmarshal(body, &v); err != nil {
		log.Printf("WARNING: failed to decode json from the api: %+v input=%q", err, string(body))
		http.Error(w,
			fmt.Sprintf("could not decode json response from the api: %+v", err),
			http.StatusInternalServerError)
		return
	}

	log.Printf("retrieved %d profile from the backend api", len(v))

	if err := tpl.ExecuteTemplate(w, "home", map[string]interface{}{
		"profiles": v,
	}); err != nil {
		log.Printf("WARNING: failed to render html template: %+v", err)
	}
}

// postHandler handles POST requests to /api/profile.
func (f *frontendServer) postHandler(w http.ResponseWriter, r *http.Request) {
	log.Printf("received request: %s %s", r.Method, r.URL.Path)
	if r.Method != http.MethodPost {
		http.Error(w, "only POST requests are supported", http.StatusMethodNotAllowed)
		return
	}

	first_name := r.FormValue("first_name")
	last_name := r.FormValue("last_name")
	avatar := r.FormValue("avatar")
	linkedin_url := r.FormValue("linkedin_url")
	company := r.FormValue("company")
	position := r.FormValue("position")
	connections := r.FormValue("connections")
	connection_dist := r.FormValue("connection_dist")
	activity := r.FormValue("activity")
	if first_name == "" {
		http.Error(w, `"first_name" not specified in the form`, http.StatusBadRequest)
		return
	}

	if first_name == "" {
		http.Error(w, `"first_name" not specified in the form`, http.StatusBadRequest)
		return
	}
	if last_name == "" {
		http.Error(w, `"last_name" not specified in the form`, http.StatusBadRequest)
		return
	}

	if err := f.saveProfile(first_name, last_name, avatar, linkedin_url, company, position, connections, connection_dist, activity); err != nil {
		http.Error(w, fmt.Sprintf("failed to save message: %+v", err), http.StatusInternalServerError)
		return
	}

	http.Redirect(w, r, "/", http.StatusFound) // redirect to homepage
}

// saveProfile makes a request to the backend to persist the message.
func (f *frontendServer) saveProfile(first_name, last_name, avatar, linkedin_url, company, position, conns, condist, activity string) error {
	entry := Profile{
		FirstName:      first_name,
		LastName:       last_name,
		Avatar:         avatar,
		LinkedInURL:    linkedin_url,
		Company:        company,
		Position:       position,
		Connections:    conns,
		ConnectionDist: condist,
		Activity:       activity,
		CreatedAt:      time.Now(),
	}
	body, err := json.Marshal(entry)
	if err != nil {
		return fmt.Errorf("failed to serialize message into json: %+v", err)
	}

	resp, err := http.Post(fmt.Sprintf("http://%s/api/profile", f.backendAddr), "application/json", bytes.NewReader(body))
	if err != nil {
		return fmt.Errorf("backend returned failure: %+v", err)
	}
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected status code from backend: %d %v", resp.StatusCode, resp.Status)
	}
	defer resp.Body.Close()
	return nil
}

// sinceDate is used in the html template to display human-friendly dates.
func sinceDate(t time.Time) string { return time.Since(t).Truncate(time.Second).String() }
