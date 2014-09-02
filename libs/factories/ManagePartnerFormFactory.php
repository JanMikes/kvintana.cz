<?php

namespace App\Factories;

use Nette,
	App,
	App\Database\Entities\PartnerEntity;

/**
 *  @author Jan Mikes <j.mikes@me.com>
 *  @copyright Jan Mikes - janmikes.cz
 */
final class ManagePartnerFormFactory extends Nette\Object
{
	use TFormSaveHandlers;


	/** @var App\Factories\FormFactory */
	private $formFactory;

	/** @var App\Database\Entities\PartnerEntity */
	private $partnerEntity;

	/** @var Nette\Database\Table\ActiveRow */
	private $row;


	public function __construct(
		FormFactory $formFactory,
		PartnerEntity $partnerEntity
	) {
		$this->formFactory = $formFactory;
		$this->partnerEntity = $partnerEntity;
	}


	public function create($id)
	{
		if ($id) {
			$this->row = $this->partnerEntity->find($id);
		}

		$form = $this->formFactory->create();

		$form->addText("name", "Název", 50, 50)
			->setRequired("Název je povinný!");

		$form->addText("url", "Odkaz", 100, 100)
			->setRequired("Název je povinný!");

		$form->addTextarea("text", "Popis", 60, 3);

		$form->addSubmit("send", $this->row ? "Upravit" : "Přidat")
			->setAttribute("class", "btn-primary")
			->onClick[] = $this->save;

		if ($this->row) {
			$form->addSubmit("sendAndContinue", "Uložit a pokračovat v editaci")
				->setAttribute("class", "btn-primary")
				->onClick[] = $this->saveAndContinue;
		}

		return $form;
	}


	public function process(Nette\Application\UI\Form $form)
	{
		$values = $form->getValues(true);

		if (!$this->row) {
			$values["ins_process"] = __METHOD__;
			$this->partnerEntity->insert($values);
		} else {
			$values["upd_process"] = __METHOD__;
			$this->row->update($values);
		}

	}

}
