<?php

namespace App\BackendModule;

use App,
	App\Factories\IPartnersListFactory,
	App\Factories\ManagePartnerFormFactory;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class PartnerPresenter extends SecuredPresenter
{
	/** @persistent int */
	public $id;

	/** @var App\Database\Entities\PartnerEntity @autowire */
	protected $partnerEntity;


	public function startup()
	{
		parent::startup();

		if ($this->view != "edit") {
			$this->id = null;
		}
	}


	public function actionEdit($id)
	{
		$this->template->partner = $this->partnerEntity->find($id);
		if (!$this->template->partner) {
			$this->redirect("default");
		}

		$defaults = $this->template->partner->toArray();

		$this["managePartnerForm"]->setDefaults($defaults);
	}


	protected function createComponentPartnersList(IPartnersListFactory $factory)
	{
		return $factory->create();
	}


	protected function createComponentManagePartnerForm(ManagePartnerFormFactory $factory)
	{
		return $factory->create($this->id);
	}
}
