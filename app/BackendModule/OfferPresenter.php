<?php

namespace App\BackendModule;

use App,
	App\Factories\IGalleriesListFactory,
	App\Factories\ManageOfferFormFactory,
	App\Factories\ManageGalleryFormFactory;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class OfferPresenter extends SecuredPresenter
{
	/** @persistent int */
	public $offerId;

	/** @persistent int */
	public $id;

	/** @var App\Database\Entities\OfferEntity @autowire */
	protected $offerEntity;

	/** @var App\Database\Entities\GalleryEntity @autowire */
	protected $galleryEntity;


	public function startup()
	{
		parent::startup();

		$this->template->offer = $this->offerEntity->find($this->offerId);
		if (!$this->offerId || !$this->template->offer) {
			$this->redirect("Dashboard:");
		}

		if ($this->view != "edit") {
			$this->id = null;
		}
	}


	public function actionEdit($id)
	{
		$this->template->gallery = $this->galleryEntity->find($id);
		if (!$this->template->gallery) {
			$this->redirect("default");
		}

		$this["manageGalleryForm"]->setDefaults($this->template->gallery->toArray());
	}


	public function actionDefault($offerId)
	{
		$this["manageOfferForm"]->setDefaults($this->template->offer->toArray());
	}


	protected function createComponentManageGalleryForm(ManageGalleryFormFactory $factory)
	{
		return $factory->create($this->offerId, $this->id);
	}


	protected function createComponentGalleriesList(IGalleriesListFactory $factory)
	{
		return $factory->create($this->offerId);
	}


	protected function createComponentManageOfferForm(ManageOfferFormFactory $factory)
	{
		return $factory->create($this->offerId);
	}
}
