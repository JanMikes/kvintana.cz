<?php

namespace App\BackendModule;

use App,
	App\Factories\ManageAboutFormFactory;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class AboutPresenter extends SecuredPresenter
{
	/** @var App\Database\Entities\AboutEntity @autowire */
	protected $aboutEntity;


	public function actionDefault()
	{
		$row = $this->aboutEntity->getLast();		
		if ($row) {
			$this["manageAboutForm"]->setDefaults($row->toArray());
		}
	}


	protected function createComponentManageAboutForm(ManageAboutFormFactory $factory)
	{
		return $factory->create();
	}
}
