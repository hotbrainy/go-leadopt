package controllers

import (
	"github.com/hotbrainy/go-leadopt/backend/models"
)

type ProfileController struct {
	/* dependencies */
}

// GET: /api/profile
func (c *ProfileController) Get() ([]models.Profile, error) {
	p := &models.Profile{}
	res, err := p.Get()
	if err != nil {
		return nil, err
	}
	return res, nil
}

// POST: /api/profile
func (c *ProfileController) Post(p models.Profile) (*models.Profile, error) {
	res, err := p.Post()

	if err != nil {
		return nil, err
	}

	return res, nil
}
