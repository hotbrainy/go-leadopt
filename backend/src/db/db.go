package db

import (
	"log"
	"os"

	"github.com/kamva/mgm/v3"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Conn struct {
	/* dependencies */
	URI string `json:"uri" bson:"uri"`
}

func (c *Conn) Init() error {
	// Setup the mgm default config
	mongoURI := (map[bool]string{true: "mongodb://localhost:27017/leadopt", false: "mongodb://" + os.Getenv("LEADOPT_DB_ADDR")})[os.Getenv("LEADOPT_DB_ADDR") == ""]

	if mongoURI == "" {
		log.Fatal("LEADOPT_DB_ADDR environment variable not specified")
	}
	log.Println(mongoURI)

	err := mgm.SetDefaultConfig(nil, "leadopt", options.Client().ApplyURI(mongoURI))

	if err != nil {
		log.Println(err)
		return err
	}
	return nil
}
