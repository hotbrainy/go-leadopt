package main

import (
	"context"
	"fmt"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type mongodb struct {
	conn *mongo.Client
}

func (m *mongodb) entries(ctx context.Context) ([]leadoptEntry, error) {
	ctx, cancel := context.WithTimeout(ctx, 10*time.Second)
	defer cancel()

	col := m.conn.Database("leadopt").Collection("entries")
	cur, err := col.Find(ctx, bson.D{}, &options.FindOptions{
		Sort: map[string]interface{}{"_id": -1},
	})
	if err != nil {
		return nil, fmt.Errorf("mongodb.Find failed: %+v", err)
	}
	defer cur.Close(ctx)

	var out []leadoptEntry
	for cur.Next(ctx) {
		var v leadoptEntry
		if err := cur.Decode(&v); err != nil {
			return nil, fmt.Errorf("decoding mongodb record failed: %+v", err)
		}
		out = append(out, v)
	}
	if err := cur.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate on mongodb cursor: %+v", err)
	}
	return out, nil
}

func (m *mongodb) addEntry(ctx context.Context, e leadoptEntry) error {
	ctx, cancel := context.WithTimeout(ctx, time.Second*3)
	defer cancel()

	col := m.conn.Database("leadopt").Collection("entries")
	if _, err := col.InsertOne(ctx, e); err != nil {
		return fmt.Errorf("mongodb.InsertOne failed: %+v", err)
	}
	return nil
}
