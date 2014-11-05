<?php

namespace Kazeto\Factory;

use Nette,
	Nette\Forms,
	Kazeto\Tables;

class ManageServiceFormFactory extends BaseAdminFormFactory implements IAdminFormFactory {

	/** @var Kazeto\Factory\BaseFormFactory */
	private $baseFormFactory;

	/** @var Kazeto\Tables\Service */
	private $serviceTable;

	/** @var Nette\Database\Table\ActiveRow */
	private $row;

	public function __construct(BaseFormFactory $baseFormFactory, Tables\Service $serviceTable)
	{
		$this->baseFormFactory = $baseFormFactory;
		$this->serviceTable = $serviceTable;
	}


	public function create($id)
	{
		if ($id) {
			$this->row = $this->serviceTable->find($id);
		}

		$form = $this->baseFormFactory->create();

		$form->addTextarea("text", "Text", 50, 4)
			->setAttribute("class", "ckeditor");


		$form->addSubmit("sendAndContinue", "Uložit")
			->setAttribute("class", "btn-primary")
			->onClick[] = $this->saveAndContinue;

		return $form;
	}


	public function process(Nette\Application\UI\Form $form)
	{
		$values = $form->getValues(true);
		$presenter = $form->presenter;

		$values["ins_process_id"] = __METHOD__;
		$this->serviceTable->insert($values);
	}

}
