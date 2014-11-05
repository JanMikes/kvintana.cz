<?php

namespace AdminModule;

use Kazeto\Factory;

class ServicePresenter extends BasePresenter {

	/** @persistent int */
	public $id;

	/** @autowire @var Kazeto\Tables\Service */
	protected $serviceTable;


	public function actionDefault()
	{
		$row = $this->serviceTable->getLast();		
		if ($row) {
			$this["manageServiceForm"]->setDefaults($row->toArray());
		}
	}


	protected function createComponentManageServiceForm(Factory\ManageServiceFormFactory $manageServiceFormFactory)
	{
		return $manageServiceFormFactory->create();
	}	
}