package models

import (
	"log"

	"github.com/kamva/mgm/v3"
	"go.mongodb.org/mongo-driver/bson"
)

type Profile struct {
	mgm.DefaultModel `bson:",inline"`

	FirstName      string `valid:"stringlength(5|20)" json:"first_name" bson:"first_name"`
	Lastname       string `valid:"stringlength(5|20)" json:"last_name" bson:"last_name"`
	Avatar         string `json:"avatar" bson:"avatar"`
	LinkedInURL    string `json:"linkedin_url" bson:"linkedin_url"`
	Company        string `json:"company" bson:"company"`
	Position       string `json:"position" bson:"position"`
	Connections    string `json:"connections" bson:"connections"`
	ConnectionDist string `json:"connection_dist" bson:"connection_dist"`
	TimeInRole     string `json:"time_in_role" bson:"time_in_role"`
	Activity       string `json:"activity" bson:"activity"`
}

func (p *Profile) Get() ([]Profile, error) {
	result := []Profile{}
	err := mgm.Coll(&Profile{}).SimpleFind(&result, bson.M{})
	if err != nil {
		log.Print(err)
		return nil, err
	}

	return result, nil
}

func (p *Profile) Post() (*Profile, error) {
	err := mgm.Coll(&Profile{}).Create(p)
	if err != nil {
		log.Print(err)
		return nil, err
	}

	return p, nil
}

func (p *Profile) Put() (*Profile, error) {
	err := mgm.Coll(&Profile{}).Update(p)
	if err != nil {
		log.Print(err)
		return nil, err
	}

	return p, nil
}
